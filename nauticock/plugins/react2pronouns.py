'''
Basic plugin that assigns users to pronoun roles on reaction

Usage:
Add reaction monitor: /r2padd <msg_id> <emoji> <role_id>
Delete reaction monitor: /r2pdel <msg_id> <emoji>
Show all reaction monitors: /r2plist

This plugin requires admin permissions
'''

from discord import NotFound, Forbidden
from discord.ext import commands
from discord.utils import get
from discord.ext.commands.errors import MissingRequiredArgument, BadArgument

from .common import BasicPlugin


class React2Pronoun(BasicPlugin):
    '''Cog that implements react2pronoun'''

    plugin_name = 'react2pronoun'
    plugin_api_ver = 0

    def __init__(self, bot):
        super().__init__(bot)
        self.settings = {}
        # Allows the plugin to revoke roles if they retract the reaction
        self.settings['revoke'] = self.get_config_var('can-revoke-role', True)
        # Restores previous roles on rejoining
        self.settings['restore'] = self.get_config_var('restore-on-rejoin',
                                                       True)
        # Ignore people who currently have roles
        self.settings['ignore-role'] = self.get_config_var('ignore-has-role',
                                                           True)
        # Ignore people who currently admin
        self.settings['ignore-admin'] = self.get_config_var('ignore-admin',
                                                            True)

        self.reactions = self.get_storage_var('reactions', [])

    async def cog_command_error(self, ctx, err):
        '''Show usage on user error for r2padd and r2pdel, otherwise raise'''
        # Ignore self invoke
        if ctx.author == self.bot.user:
            return
        # Ignore non-admins
        if not ctx.author.guild_permissions.administrator:
            return

        if ctx.command.name == 'r2padd' and (
                isinstance(err, MissingRequiredArgument)
                or isinstance(err, BadArgument)):
            await ctx.channel.send(
                '```Usage: /r2padd <msg_id> <emoji> <role_id>```')
        elif ctx.command.name == 'r2pdel' and (
                isinstance(err, MissingRequiredArgument)
                or isinstance(err, BadArgument)):
            await ctx.channel.send(
                '```Usage: /r2pdel <msg_id> <emoji>```')
        else:
            raise err

    @commands.command()
    async def r2padd(self, ctx, msg_id: int, emoji, role: int):
        '''Used to add a reaction monitor'''
        # Ignore self invoke
        if ctx.author == self.bot.user:
            return
        # Ignore non-admins
        if not ctx.author.guild_permissions.administrator:
            return

        # Check if the message/emoji set already exists
        for reaction in self.reactions:
            if reaction['msg_id'] == msg_id and reaction['emoji'] == emoji:
                await ctx.channel.send('Reaction monitor already exists')
                return

        # Sanity check for roles
        if not get(ctx.guild.roles, id=role):
            await ctx.channel.send('Role ID not found')
            return

        # Sanity check for message
        for channel in ctx.guild.text_channels:
            try:
                await channel.fetch_message(msg_id)
            except (NotFound, Forbidden):
                continue
            # We've found everything, add to database
            reaction = {
                'msg_id': msg_id,
                'guild_id': ctx.guild.id,
                'emoji': emoji,
                'role_id': role,
                'restore': {}
            }
            self.reactions.append(reaction)
            # Since we modified a list, mark it as dirty
            self.mark_plugin_storage_dirty()
            self.flush_storage()
            await ctx.channel.send('Reaction monitor added')
            return

        # Message doesn't exist
        await ctx.channel.send(
            ('Message ID not found, make sure Nauticock has valid '
             'permissions to see the message'))

    @commands.command()
    async def r2pdel(self, ctx, msg_id: int, emoji):
        '''Used to delete a reaction monitor'''
        # Ignore self invoke
        if ctx.author == self.bot.user:
            return
        # Ignore non-admins
        if not ctx.author.guild_permissions.administrator:
            return

        # We will be deleting, so make a copy before iterating
        for reaction in self.reactions.copy():
            # Make sure the admin is deleting something he actual administers
            if reaction['guild_id'] != ctx.guild.id:
                continue
            # Found the reaction monitor
            if reaction['msg_id'] == msg_id and reaction['emoji'] == emoji:
                self.reactions.remove(reaction)
                # Since we modified a list, mark it as dirty
                self.mark_plugin_storage_dirty()
                self.flush_storage()
                await ctx.channel.send('Reaction monitor removed')
                return

        # Never found reaction monitor
        await ctx.channel.send('Reaction monitor does not exist')

    @commands.command()
    async def r2plist(self, ctx):
        '''Used to list all reaction monitors'''
        # Ignore self invoke
        if ctx.author == self.bot.user:
            return
        # Ignore non-admins
        if not ctx.author.guild_permissions.administrator:
            return

        # Try to keep discord calls to a minimum, so group the message
        response = 'react2pronoun monitored reactions:\n```'
        for reaction in self.reactions:
            # Only print stuff in the current guild
            if reaction['guild_id'] != ctx.guild.id:
                continue
            response += f'msg_id: {reaction["msg_id"]}\n'
            response += f'emoji: {reaction["emoji"]}\n'
            response += f'role_id: {reaction["role_id"]}\n\n'
        response += '\n```'
        # Send the grouped message
        await ctx.channel.send(response)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        '''Called when a reaction is added, even if not in cache'''
        # Check our database of reactions
        for reaction in self.reactions:
            if event.message_id != reaction['msg_id'] \
                    or event.emoji.name != reaction['emoji']:
                # Wrong one, keep iterating
                continue

            guild = self.bot.get_guild(event.guild_id)
            member = guild.get_member(event.user_id)

            # If the proper config is set then ignore admins
            if self.settings['ignore-admin'] \
                    and member.guild_permissions.administrator:
                self.log_info(f'Ignoring admin {member.name}')
            # Also ignore unprivileged users
            elif not member.guild_permissions.send_messages:
                self.log_info('Ignoring unprivilaged user {member.name}')
            # Add the new role
            else:
                role = guild.get_role(reaction['role_id'])
                if role:
                    self.log_info(f'Adding role {role.name} to {member.name}')
                    await member.add_roles(role, reason='react2pronoun')
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):
        '''Called when a reaction is removed, even if not in cache'''
        # Iterate again through monitors
        for reaction in self.reactions:
            if event.message_id != reaction['msg_id'] \
                    or event.emoji.name != reaction['emoji']:
                continue

            guild = self.bot.get_guild(event.guild_id)
            member = guild.get_member(event.user_id)
            role = guild.get_role(reaction['role_id'])

            # Ignore admin reacts
            if self.settings['ignore-admin'] \
                    and member.guild_permissions.administrator:
                self.log_info(f'Ignoring admin {member.name}')
	    # Ignore if the user does not have this pronoun role
            elif role not in member.roles:
                self.log_info(f'{member.name} does not have role {role.name}')
            # Revoke the pronoun
            else:
                self.log_info(f'Revoking {role.name} from {member.name}')
                await member.remove_roles(role, reason='react2pronoun revoke')
            return
