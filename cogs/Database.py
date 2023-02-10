import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
import os, sys
import apikeys, utils

class Database(commands.Cog):

    serverIdList = apikeys.serverIdList()
            
    def __init__(self, client):
        self.client = client

        self.path_to_db = "./db/"
        self.json_filename = "./db/db.json"
        if os.path.exists(self.json_filename) == False:
            f = open(self.json_filename, 'a')
            f.write("{}")
            f.close()
        
        self.db = utils.load_json(self.json_filename)
    
    @nextcord.slash_command(name="get", description="Retrieve an entry from the database", guild_ids=serverIdList)
    async def help(self, interaction: Interaction, key:str):
        if key in self.db["entry"]:
            await interaction.response.send_message(files=[nextcord.File(self.path_to_db + key + self.db["entry"][key]["extension"])])
        else:
            await interaction.response.send_message("No such file found for key: \"" + key + "\"")

def setup(client):
    client.add_cog(Database(client))