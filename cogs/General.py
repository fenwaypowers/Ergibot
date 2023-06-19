import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.utils import get
import os, sys
import apikeys, utils, random

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
        path = "db/kevin"
        if os.path.exists(path):
            choice = random.choice(os.listdir(path))

            if random.randint(1,100000) == 1:
                #ultra-rare kevin code here
                pass

            await interaction.response.send_message("Here is your Kevin.")
            await interaction.channel.send(file=nextcord.File(f"{path}/{choice}"))
        else:
            await interaction.response.send_message("Command failed.")

    @nextcord.slash_command(name = "joe", description = "Displays a random image of Joe.", guild_ids=['912896088439160882'])
    async def joe(self, interaction: Interaction):
        path = "db/joe"
        if os.path.exists(path):
            choice = random.choice(os.listdir(path))

            await interaction.response.send_message("Here is your Joe.")
            await interaction.channel.send(file=nextcord.File(f"{path}/{choice}"))
        else:
            await interaction.response.send_message("Command failed.")

def setup(client):
    client.add_cog(General(client))
    