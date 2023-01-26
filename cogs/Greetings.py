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

    @commands.Cog.listener()
    async def on_member_join(self, member, guild_ids=serverIdList):
        # For this function to work, you need to enable intents in the developer portal.
        # https://discord.com/developers/applications
        # Bot > Bot > Presence & Server Members Intents > Toggle On

        guild = member.guild
        roles = guild.roles

        role_index = -1
        for i in range(0, len(roles)): #roles is not iterable :/
            role = str(roles[i])
            if role == 'Friends':
                role_index = i
        
        if role_index != -1:
            await member.add_roles(roles[role_index])

def setup(client):
    client.add_cog(Greetings(client))