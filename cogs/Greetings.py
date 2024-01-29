import nextcord
from nextcord.ext import commands
import globals

class Greetings(commands.Cog):

    serverIdList = globals.config.servers.server_list
            
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Greetings(client))
    