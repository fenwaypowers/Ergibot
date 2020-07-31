'''
Basic plugin that allows admins to say things through Nauticock

Usage: /adminsay <channel> <message>

send_message permission is required for Nauticock in channel specified
administrator permission is required for user in channel specified
'''
from discord import TextChannel
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, BadArgument

from .common import BasicPlugin


class AdminSay(BasicPlugin):
    '''Cog class for adminsay'''

    plugin_name = 'adminsay'
    plugin_api_ver = 0

    # Handle errors, including user errors
    async def cog_command_error(self, ctx, err):
        if ctx.author == self.bot.user:
            return
        if not ctx.author.guild_permissions.administrator:
            return

        if isinstance(err, MissingRequiredArgument) \
                or isinstance(err, BadArgument):
            await ctx.channel.send('```Usage: /adminsay <channel> <msg>```')

    # Actual command handler
    @commands.command()
    async def adminsay(self, ctx, channel: TextChannel, *, msg):
        if ctx.author == self.bot.user:
            return
        if not ctx.author.guild_permissions.administrator:
            return

        self.log_info(f'{ctx.author}: /adminsay #{channel} {msg}')
        await channel.send(msg)
