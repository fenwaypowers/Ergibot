import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.utils import get
import os, sys
import apikeys, utils

class Admin(commands.Cog):

    serverIdList = apikeys.serverIdList()
    def __init__(self, client):
        self.client = client

        self.ROLE_FOR_ADMIN_PERMS = "THE COUNCIL"
        self.NO_PERMS_MSG = "You do not have permission to use this command!"
    
    @nextcord.slash_command(name = "botsay", description = "Make the bot send a message", guild_ids=serverIdList)
    async def botsay(self, interaction: Interaction, msg:str, channel_id:str):
        channel_str = channel_id
        role = get(interaction.user.roles, name=self.ROLE_FOR_ADMIN_PERMS)
        if role in interaction.user.roles:
            channel = self.client.get_channel(int(channel_id))
            await channel.send(msg)
            await interaction.response.send_message("Message \"" + msg + "\" has been sent to channel " + channel_str + ".")
        else:
            await interaction.response.send_message(self.NO_PERMS_MSG)

def setup(client):
    client.add_cog(Admin(client))