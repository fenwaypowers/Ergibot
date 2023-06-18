import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.utils import get
import os, sys
import apikeys, utils
from database import *
from ergicoin import *
from games import *

class Games(commands.Cog):
    serverIdList = apikeys.serverIdList()

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "rps", description = "Play Rock Paper Scissors with the bot!", guild_ids=serverIdList)
    async def rps(self, interaction: Interaction, bet: int = 0):
        conn = create_connection()

        # Check if the user is in the money table
        userid = str(interaction.user.id)
        username = interaction.user.name

        # Check if the user has enough money to bet
        user_money = get_user_money(conn, userid, username)
        if validate_bet(user_money, bet):
            await interaction.response.send_message("You don't have enough coins to make that bet, or you used a negative value.")
            close_connection(conn)
            return

        view = RpsInteractions(interaction.user)

        await interaction.response.send_message("Choose Rock, Paper, or Scissors:", view=view)
        await view.wait()

        if view.value is None:
            await interaction.channel.send("Nothing chosen.")
            return
        elif view.value:

            # Start a game of RPS
            game = Rps(view.value)
            result = game.rps(bet)

            # Handle the bet
            if game.win_state == 2:  # Player won
                update_user_money(conn, userid, user_money + bet)
            elif game.win_state == 3:  # Player lost
                update_user_money(conn, userid, user_money - bet)
            
            await interaction.channel.send(result)

        close_connection(conn)

    @nextcord.slash_command(name = "wallet", description = "Show how much ergicoins user has in wallet.", guild_ids=serverIdList)
    async def wallet(self, interaction: Interaction, member: nextcord.Member=None):
        if member is None:
            userid = str(interaction.user.id)
            username = str(interaction.user.name)
        else:
            userid = str(member.id)
            username = str(member.name)

        conn = create_connection()
        
        coins = get_user_money(conn, userid, username)
        close_connection(conn)
        
        await interaction.response.send_message(f"{member.name if member else interaction.user.name} has {coins} ergicoins.")
    
    @nextcord.slash_command(name = "transfer", description = "Transfer ergicoins to another user.", guild_ids=serverIdList)
    async def transfer(self, interaction: Interaction, member: nextcord.Member, amount: int):
        conn = create_connection()

        initialize_user_money(conn, member.name, member.id)
        initialize_user_money(conn, interaction.user.name, interaction.user.id)
        
        if transfer_coins(conn, interaction.user.id, member.id, amount):
            await interaction.response.send_message(f"{interaction.user.name}, you have successfully sent {amount} ergicoins to {member.name}.")
        else:
            await interaction.response.send_message(f"Error occured during transfer. Please make sure that after the transfer you will have a minimum of 1000 ergicoins.")
        close_connection(conn)

def setup(client):
    client.add_cog(Games(client))
