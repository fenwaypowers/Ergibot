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

class BjInteractions(nextcord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.value = None
        self.user = user
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Stand")
    async def rock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "stand"
            self.stop()
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Hit")
    async def paper(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.user.id:
            self.value = "hit"
            self.stop()

class Blackjack():
    deckcards = ['A'] * 4 + ['K'] * 4  + ['Q'] * 4 + ['J'] * 4 + ['2'] * 4 + ['3'] * 4 + ['4'] * 4 + ['5'] * 4 + ['6'] * 4 + ['7'] * 4 + ['8'] * 4 + ['9'] * 4 + ['10'] * 4
    cardvalues = {
    'K':10,
    'Q':10,
    'A':11,
    'J':10,
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    '10':10
    }

    def __init__(self, user, bet):
        self.user = user
        self.bet = bet
        self.deck = self.deckcards
        random.shuffle(self.deck)
        self.playerhand = []
        self.dealerhand = []
        self.playerscore = 0
        self.dealerscore = 0
        self.winner = None
        self.game_over = False
        self.startGame()

    def pickCard(self):
        return self.deck.pop()      

    def playerPick(self):
        self.playerhand.append(self.pickCard())

    def dealerPick(self):
        self.dealerhand.append(self.pickCard())

    def startGame(self):
        for i in range(0, 2):
            self.playerPick()
        
        for i in range(0, 2):
            self.dealerPick()

        self.checkForWinner()

    def calcScore(self, hand):
        score = sum(self.cardvalues[card] for card in hand)
        if 'A' in hand:
            if score > 21:
                score -= 10 * hand.count('A')
        return score

    def checkForWinner(self):
        self.playerscore = self.calcScore(self.playerhand)
        self.dealerscore = self.calcScore(self.dealerhand)

        if self.playerscore == 21:
            self.winner = self.user
            self.game_over = True
        elif self.dealerscore == 21:
            self.winner = 'Dealer'
            self.game_over = True
        elif self.playerscore > 21:
            self.winner = 'Dealer'
            self.game_over = True
        elif self.dealerscore > 21:
            self.winner = self.user
            self.game_over = True
        elif self.game_over:  # When player chooses to 'stand'
            if self.playerscore > self.dealerscore:
                self.winner = self.user
            elif self.playerscore < self.dealerscore:
                self.winner = 'Dealer'
            else:
                self.winner = 'Push'

    def stringHands(self):
        strng = ""
        if not self.game_over:
            concealedhand = [self.dealerhand[0], "?"]
            strng += f"Dealer's hand: {concealedhand}"  # Concealment is done here
        else:
            strng += f"Dealer's hand: {self.dealerhand}"

        strng += f"\n{self.user.name}'s hand: {self.playerhand}"

        return strng

    def hit(self):
        self.playerPick()
        self.checkForWinner()

    def stand(self):
        self.game_over = True
        self.dealerPlays()

    def dealerPlays(self):
        while self.calcScore(self.dealerhand) < 17:
            self.dealerPick()
        self.checkForWinner()