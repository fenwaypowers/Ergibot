import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.utils import get
import globals

class Admin(commands.Cog):

    serverIdList = globals.config.servers.server_list
    adminRoles = globals.config.admin.roles

    def __init__(self, client):
        self.client = client
        self.NO_PERMS_MSG = "You do not have permission to use this command!"
    
    @nextcord.slash_command(name="botsay", description="Make the bot send a message", guild_ids=serverIdList)
    async def botsay(self, interaction: Interaction, msg: str, channel_id: str):
        try:
            # Attempt to convert the channel_id string to an integer
            channel_id_int = int(channel_id)
            # Check if the user has any of the roles defined in adminRoles
            user_roles = set(role.name for role in interaction.user.roles)
            if user_roles.intersection(self.adminRoles):
                channel = self.client.get_channel(channel_id_int)
                if channel:  # Make sure the channel exists
                    await channel.send(msg)
                    await interaction.response.send_message(f"Message '{msg}' has been sent to channel {channel_id}.")
                else:
                    await interaction.response.send_message("The channel ID provided does not exist.", ephemeral=True)
            else:
                await interaction.response.send_message(self.NO_PERMS_MSG, ephemeral=True)
        except ValueError:
            # If conversion fails, send an ephemeral message to the user
            await interaction.response.send_message("You have entered an invalid channel ID. Please enter a valid integer.", ephemeral=True)

def setup(client):
    client.add_cog(Admin(client))
