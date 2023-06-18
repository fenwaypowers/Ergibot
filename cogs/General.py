import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.utils import get
import os, sys
import apikeys, utils

class General(commands.Cog):
    serverIdList = apikeys.serverIdList()

    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name = "help", description = "Help for using the bot", guild_ids=serverIdList)
    async def help(self, interaction: Interaction):
        help_message = '''Thanks for using **Ergibot**. 
The bot was originally written in 2020, but as of 2023 has been completely re-written from the ground up to work with the new discord bot API and using nextcord rather than discord.py.
'''
        await interaction.response.send_message(help_message)

    @nextcord.slash_command(name = "kevin", description = "Displays a random image of Kevin. Try to get the ultra-rare Kevin!", guild_ids=serverIdList)
    async def kevin(self, interaction: Interaction):
        await interaction.response.send_message("Not yet implemented.")

def setup(client):
    client.add_cog(General(client))
    