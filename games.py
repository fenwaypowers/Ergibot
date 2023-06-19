import random
import nextcord

class RpsInteractions(nextcord.ui.View):
    def __init__(self, player_one, player_two=None):
        super().__init__()
        self.move_player_one = None
        self.move_player_two = None
        self.player_one = player_one
        self.player_two = player_two
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Rock", emoji="🪨")
    async def rock(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.process_interaction("r", interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Paper", emoji="📰")
    async def paper(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.process_interaction("p", interaction)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, label="Scissors", emoji="✂")
    async def scissors(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.process_interaction("s", interaction)
    
    async def process_interaction(self, move, interaction):
        if interaction.user.id == self.player_one.id and self.move_player_one is None:
            self.move_player_one = move
            if self.player_two is None:
                self.stop()
        elif self.player_two is not None and interaction.user.id == self.player_two.id and self.move_player_two is None:
            self.move_player_two = move

        if self.player_two is not None and self.move_player_one is not None and self.move_player_two is not None:
            self.stop()

class Rps:
    GAME_ERROR = 0
    GAME_TIE = 1
    PLAYER_ONE_WIN = 2
    PLAYER_TWO_WIN = 3

    valid_moves = ['r', 'p', 's']

    def __init__(self, move_player_one, username=None, username2=None, move_player_two=None):
        self.move_player_one = move_player_one[0].lower()
        self.move_computer = random.choice(self.valid_moves)
        self.move_player_two = move_player_two[0].lower() if move_player_two else None
        self.username = username
        self.username2 = username2
        self.win_state = self.calculate_result()

    def calculate_result(self):
        move_player_one = self.move_player_one
        move_player_two = self.move_player_two
        if move_player_one not in self.valid_moves:
            return self.GAME_ERROR

        move_computer = move_player_two if move_player_two else self.move_computer
        
        beats = {
            'r' : 's',
            'p' : 'r',
            's' : 'p'
        }

        if move_player_one == move_computer:
            return self.GAME_TIE
        elif beats[move_player_one] == move_computer:
            return self.PLAYER_ONE_WIN
        else:
            return self.PLAYER_TWO_WIN

    def rps(self, bet, opponent=None):
        if bet < 0:
            return "Invalid Bet"

        move = self.move_player_one
        other_move = self.move_player_two if opponent else self.move_computer
        state = self.win_state

        pretty_print = {
            'r' : 'Rock',
            'p' : 'Paper',
            's' : 'Scissors'
        }

        if self.move_player_two == None:
            if state == self.GAME_ERROR:
                return f"A problem occured."
            if state == self.GAME_TIE:
                return f"Tie! We both went {pretty_print[move]}!"
            elif state == self.PLAYER_ONE_WIN:
                return f"You went {pretty_print[move]}, and I went {pretty_print[other_move]}. You win {bet} ergicoin!"
            elif state == self.PLAYER_TWO_WIN:
                return f"You went {pretty_print[move]}, and I went {pretty_print[other_move]}. You lose {bet} ergicoin."
        else:
            if state == self.GAME_ERROR:
                return f"A problem occured."
            if state == self.GAME_TIE:
                return f"Tie! {self.username} and {self.username2} both went {pretty_print[move]}!"
            elif state == self.PLAYER_ONE_WIN:
                return f"{self.username} went {pretty_print[move]}, and {self.username2} went {pretty_print[other_move]}. {self.username} wins {bet} ergicoin!"
            elif state == self.PLAYER_TWO_WIN:
                return f"{self.username} went {pretty_print[move]}, and {self.username2} went {pretty_print[other_move]}. {self.username2} wins {bet} ergicoin!"

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
