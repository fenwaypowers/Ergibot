import random
import nextcord

class RpsInteractions(nextcord.ui.View):
    def __init__(self, user, user2=None):
        super().__init__()
        self.value = None
        self.value2 = None
        self.user = user
        self.user2 = user2
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Rock", emoji="🪨")
    async def rock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.process_interaction("r", interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Paper", emoji="📰")
    async def paper(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.process_interaction("p", interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Scissors", emoji="✂")
    async def scissors(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.process_interaction("s", interaction)
    
    async def process_interaction(self, value, interaction):
        if interaction.user.id == self.user.id and self.value is None:
            self.value = value
            # If user2 is None, stop after the first user's interaction
            if self.user2 is None:
                self.stop()
        elif self.user2 is not None and interaction.user.id == self.user2.id and self.value2 is None:
            self.value2 = value

        # If both users have made a selection, stop the view
        if self.user2 is not None and self.value is not None and self.value2 is not None:
            self.stop()

class Rps:

    valid_moves = ['r', 'p', 's']

    def __init__(self, move, username=None, username2=None, move2=None):
        self.move = move[0].lower()
        self.com = random.choice(self.valid_moves)
        self.move2 = move2[0].lower() if move2 else None
        self.win_RPS()
        self.username = username
        self.username2 = username2

    def rps(self, bet, user2=None):
        if bet < 0:
            return "Invalid Bet"

        move = self.move[0].lower()
        other_move = self.move2 if user2 else self.com
        state = self.win_state

        pretty_print = {
            'r' : 'Rock',
            'p' : 'Paper',
            's' : 'Scissors'
        }

        if self.move2 == None:
            if state == 0:
                return f"A problem occured."
            if state == 1:
                return f"Tie! We both went {pretty_print[move]}!"
            elif state == 2:
                return f"You went {pretty_print[move]}, and I went {pretty_print[other_move]}. You win {bet} ergicoin!"
            elif state == 3:
                return f"You went {pretty_print[move]}, and I went {pretty_print[other_move]}. You lose {bet} ergicoin."
        else:
            if state == 0:
                return f"A problem occured."
            if state == 1:
                return f"Tie! {self.username} and {self.username2} both went {pretty_print[move]}!"
            elif state == 2:
                return f"{self.username} went {pretty_print[move]}, and {self.username2} went {pretty_print[other_move]}. {self.username} wins {bet} ergicoin!"
            elif state == 3:
                return f"{self.username} went {pretty_print[move]}, and {self.username2} went {pretty_print[other_move]}. {self.username2} wins {bet} ergicoin!"

    def pvp(self):
        if not self.move2:
            return "Error: Player 2 not found"
        return self.rps(0, user2=True)  # Zero bet for player vs player. Change as required.

    def win_RPS(self):
        move = self.move
        move2 = self.move2
        if move not in self.valid_moves:
            self.win_state = 0
            return

        com_move = move2 if move2 else self.com
        
        beats = {
            'r' : 's',
            'p' : 'r',
            's' : 'p'
        }

        if move == com_move:
            self.win_state = 1  # Tie state
        elif beats[move] == com_move:
            self.win_state = 2  # Player1 won
        else:
            self.win_state = 3  # Player1 loses

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

    cardemojis = {
        'K': '<:k_:1120154858499084358>',
        'Q': '<:q_:1120154861783236640>',
        'A': '<:a_:1120154855634378826>',
        'J': '<:j_:1120154857521819738>',
        '2': '<:2_:1120154971850162226>',
        '3': '<:3_:1120155035041538108>',
        '4': '<:4_:1120155021057720361>',
        '5': '<:5_:1120154860617220126>',
        '6': '<:6_:1120154915940089947>',
        '7': '<:7_:1120154863989436506>',
        '8': '<:8_:1120154862894727219>',
        '9': '<:9_:1120154859296006280>',
        '10': '<:10:1120154868041134080>',
        '?': ':question:'
    }

    def __init__(self, user):
        self.user = user
        self.deck = self.deckcards.copy()
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
            concealedhand = f"{self.cardemojis[self.dealerhand[0]]} {self.cardemojis['?']}"
            strng += f"Dealer's hand: {concealedhand}"  # Concealment is done here
        else:
            strng += f"Dealer's hand: {self.prettyPrintHand(self.dealerhand)}"

        strng += f"\n{self.user.name}'s hand: {self.prettyPrintHand(self.playerhand)}"

        return strng

    def prettyPrintHand(self, hand):
        new = ""
        for card in hand:
            new += f"{self.cardemojis[card]} "

        return new

    def hit(self):
        self.playerPick()
        self.checkForWinner()

    def stand(self):
        self.game_over = True
        self.dealerPlays()
        self.checkForWinner()

    def dealerPlays(self):
        while self.calcScore(self.dealerhand) < 17:
            self.dealerPick()
        self.checkForWinner()
