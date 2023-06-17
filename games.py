import random
import nextcord

class RpsInteractions(nextcord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.value = None
        self.user = user
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Rock", emoji="🪨")
    async def rock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "r"
            self.stop()
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Paper", emoji="📰")
    async def paper(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "p"
            self.stop()

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Scissors", emoji="✂")
    async def scissors(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "s"
            self.stop()

class Rps():

    valid_moves = ['r', 'p', 's']
    win_state = 0

    def __init__(self, move):
        self.move = move[0].lower()
        self.com = random.choice(self.valid_moves)
        self.win_RPS()

    def rps(self, bet):
        move = self.move[0].lower()
        
        com_move = random.choice(self.valid_moves)

        state = self.win_state

        pretty_print = {
            'r' : 'Rock',
            'p' : 'Paper',
            's' : 'Scissors'
        }

        if state == 0:
            return f"A problem occured."
        if state == 1:
            return f"Tie! We both went {pretty_print[move]}!"
        elif state == 2:
            return f"You went {pretty_print[move]}, and I went {pretty_print[com_move]}. You win {bet} ergicoin!"
        elif state == 3:
            return f"You went {pretty_print[move]}, and I went {pretty_print[com_move]}. You lose {bet} ergicoin."

    def win_RPS(self):
        move = self.move
        if move not in self.valid_moves:
            return # win_state stays 0
        
        com_move = self.com
        beats = {
            'r' : 's',
            'p' : 'r',
            's' : 'p'
        }

        if move == com_move:
            self.win_state = 1 # Tie state
        elif beats[move] == com_move:
            self.win_state = 2 # Player won
        else:
            self.win_state = 3 # Player loses
            