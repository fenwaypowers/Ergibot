import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
import os, sys
import apikeys

class Greetings(commands.Cog):

    serverIdList = apikeys.serverIdList()
            
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(Greetings(client))