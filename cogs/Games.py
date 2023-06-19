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

    @nextcord.slash_command(name = "blackjack", description = "Play Blackjack with the bot!", guild_ids=serverIdList)
    async def blackjack(self, interaction: Interaction, bet: int = 0):
        conn = create_connection()

        userid = str(interaction.user.id)
        username = interaction.user.name

        initialize_user_money(conn, interaction.user.name, interaction.user.id)

        # Check if the user has enough money to bet
        user_money = get_user_money(conn, userid, username)
        if validate_bet(user_money, bet):
            await interaction.response.send_message("You don't have enough coins to make that bet, or you used a negative value.")
            close_connection(conn)
            return
        
        close_connection(conn)

        bj = Blackjack(interaction.user)

        if bj.winner == interaction.user:
            nat_bet = int(bet*1.5)
            await interaction.response.send_message(f"You got a natural blackjack! You win {nat_bet} ergicoins!")
            conn = create_connection()
            update_user_money(conn, userid, user_money + nat_bet)
            close_connection(conn)
        elif bj.winner == "Push":
            await interaction.response.send_message(f"You matched the dealer, push.")
        elif bj.winner == "Dealer":
            await interaction.response.send_message(f"You lost against the dealer's natural blackjack. You lose {bet} ergicoins.")
            conn = create_connection()
            update_user_money(conn, userid, user_money - bet)
            close_connection(conn)
        else:
            view = BjInteractions(interaction.user)
            await interaction.response.send_message(bj.stringHands(), view=view)
            while bj.winner == None:
                if not bj.game_over:
                    await view.wait()

                    if view.value == "hit":
                        bj.hit()
                    elif view.value == "stand":
                        bj.stand()
                    else:
                        return
                else:
                    bj.dealerPlays()

                view = BjInteractions(interaction.user)
                if bj.winner == None:
                    await interaction.channel.send(bj.stringHands(), view=view)
                else:
                    await interaction.channel.send(bj.stringHands())
            
            if bj.winner == interaction.user:
                await interaction.channel.send(f"You win {bet} ergicoins!")
                conn = create_connection()
                update_user_money(conn, userid, user_money + bet)
                close_connection(conn)
            elif bj.winner == "Push":
                await interaction.channel.send(f"You matched the dealer, push.")
            elif bj.winner == "Dealer":
                await interaction.channel.send(f"You lose {bet} ergicoins.")
                conn = create_connection()
                update_user_money(conn, userid, user_money - bet)
                close_connection(conn)

    @nextcord.slash_command(name = "rps", description = "Play Rock Paper Scissors with the bot or someone else!", guild_ids=serverIdList)
    async def rps(self, interaction: Interaction, bet: int = 0, opponent: nextcord.Member = None):
        conn = create_connection()

        # Check if the user is in the money table
        user_id = str(interaction.user.id)
        user_name = interaction.user.name
            
        # Check if the user has enough money to bet
        initialize_user_money(conn, user_name, user_id)
        user_money = get_user_money(conn, user_id, user_name)
        if validate_bet(user_money, bet):
            await interaction.response.send_message("You don't have enough coins to make that bet, or you used a negative value.")
            close_connection(conn)
            return
        
        # Check if the second user exists, then initialize player
        interaction_view = RpsInteractions(interaction.user, opponent)

        if opponent != None:
            opponent_id = str(opponent.id)
            opponent_name = opponent.name

            initialize_user_money(conn, opponent_name, opponent_id)

            opponent_money = get_user_money(conn, opponent_id, opponent_name)
            if validate_bet(opponent_money, bet):
                await interaction.response.send_message("The opponent doesn't have enough coins to accept that bet, or you used a negative value.")
                close_connection(conn)
                return
            
            await interaction.response.send_message(f"{interaction.user.mention} has challenged you, {opponent.mention} to Rock Paper Scissors! The bet is {bet}. By clicking a button, you accept the bet.", view=interaction_view)
            
            await interaction_view.wait()

            if interaction_view.move_player_one is None or interaction_view.move_player_two is None:
                await interaction.channel.send("Nothing chosen.")
                return
            elif interaction_view.move_player_one and interaction_view.move_player_two:

                # Start a game of RPS
                game = Rps(interaction_view.move_player_one, user_name, opponent_name, interaction_view.move_player_two)
                result = game.rps(bet, opponent)

                # Handle the bet
                if game.win_state == Rps.PLAYER_ONE_WIN:  # Player1 won
                    update_user_money(conn, user_id, user_money + bet)
                    update_user_money(conn, opponent_id, opponent_money - bet)
                elif game.win_state == Rps.PLAYER_TWO_WIN:  # Player1 lost
                    update_user_money(conn, user_id, user_money - bet)
                    update_user_money(conn, opponent_id, opponent_money + bet)
                
                await interaction.channel.send(result)
        else:
            await interaction.response.send_message("Choose Rock, Paper, or Scissors:", view=interaction_view)
            await interaction_view.wait()

            if interaction_view.move_player_one is None:
                await interaction.channel.send("Nothing chosen.")
                return
            elif interaction_view.move_player_one:
                
                # Start a game of RPS
                game = Rps(interaction_view.move_player_one)
                result = game.rps(bet)

                # Handle the bet
                if game.win_state == Rps.PLAYER_ONE_WIN:  # Player won
                    update_user_money(conn, user_id, user_money + bet)
                elif game.win_state == Rps.PLAYER_TWO_WIN:  # Player lost
                    update_user_money(conn, user_id, user_money - bet)
                
                await interaction.channel.send(result)

            close_connection(conn)


    @nextcord.slash_command(name = "wallet", description = "Show how many ergicoins a user has in wallet.", guild_ids=serverIdList)
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
