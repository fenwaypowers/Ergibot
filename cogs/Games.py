import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.utils import get
import os, sys
import apikeys, utils
from database import *
from ergicoin import *

class Games(commands.Cog):
    serverIdList = apikeys.serverIdList()

    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name = "rps", description = "Play Rock Paper Scissors with the bot!", guild_ids=serverIdList)
    async def help(self, interaction: Interaction, bet=0):
        await interaction.response.send_message(f"Not implemented yet.")

    @nextcord.slash_command(name = "wallet", description = "Show how much money user has in wallet.", guild_ids=serverIdList)
    async def wallet(self, interaction: Interaction, member: nextcord.Member=None):
        if member is None:
            userid = str(interaction.user.id)
            username = str(interaction.user.name)
        else:
            userid = str(member.id)
            username = str(member.name)

        conn = create_coin_connection()
        
        coins = get_user_money(conn, userid, username)
        close_coin_connection(conn)
        
        await interaction.response.send_message(f"{member.name if member else interaction.user.name} has {coins} coins.")
    
    @nextcord.slash_command(name = "transfer", description = "Transfer ergicoin to another user.", guild_ids=serverIdList)
    async def transfer(self, interaction: Interaction, member: nextcord.Member, amount: int):
        conn = create_coin_connection()

        initialize_user_money(conn, member.name, member.id)
        initialize_user_money(conn, interaction.user.name, interaction.user.id)
        
        transfer_coins(conn, interaction.user.id, member.id, amount)
        await interaction.response.send_message(f"{interaction.user.name}, you have successfully sent {amount} ergicoins to {member.name}.")
        close_coin_connection(conn)

def setup(client):
    client.add_cog(Games(client))
