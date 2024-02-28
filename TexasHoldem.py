import random
import time
import copy
from colorama import init, Fore

init()

# SETUP GAME -------------------------------------------------------------------------------
# Creating deck
ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
suits = ['♥', '♦', '♠', '♣']

# Asks for decks and player
numDecks = int(input('How many decks do you want to use? '))
numPlayers = int(input('How opponents do you want? '))

# Function to value each royal card 
def numRank(card):
    if card == 'J':
        return 11
    elif card == 'Q':
        return 12
    elif card == 'K':
        return 13
    elif card == 'A':
        return 14
    elif card == '?':
        return 0
    else:
        return card if isinstance(card, int) else int(card)


# VISUAL FUNCTIONS to make it nice -------------------------------------------------------------------------------

# Visual aspect, creates a line of each card adds it to a list as 'data', and then reformates it when printing
def cardVisual(number, suit):
    number_str = str(number) if number != '?' else '?'
    if len(number_str) == 1:
        # Single-digit number
        line1 = f'┌─────────┐ '
        line2 = f'│ {number_str}{suit}      │ '.format(number, suit)
        line3 = f'│         │ '
        line4 = f'│         │ '
        line5 = f'│         │ '
        line6 = f'│         │ '
        line7 = f'│      {number_str}{suit} │ '.format(number, suit)
        line8 = f'└─────────┘ '
    else:
        # Double-digit number
        line1 = f'┌─────────┐ '
        line2 = f'│ {number_str}{suit}     │ '.format(number, suit)
        line3 = f'│         │ '
        line4 = f'│         │ '
        line5 = f'│         │ '
        line6 = f'│         │ '
        line7 = f'│     {number_str}{suit} │ '.format(number, suit)
        line8 = f'└─────────┘ '

    # Pad shorter lines with spaces to ensure all lines have the same length
    lines = [line1, line2, line3, line4, line5, line6, line7, line8]
    return lines


# Finds the card tuple and data inside from given input (tempPC), and then calls the card visual function 
def cardCount(tempPC):
        result_list = []

        for card_info in tempPC:
            lines = cardVisual(card_info[0], card_info[1])
            result_list.extend(lines)

        return result_list

# Function for print all, used in player cards, table, and opponents
def ASCIIPrintFormat(blankCards):
    if not all(isinstance(card, tuple) for card in blankCards):
        return
    thing_card_lines = cardCount(blankCards)
    max_lengths = [max(len(line) for line in thing_card_lines[i * 8:(i + 1) * 8]) for i in range(len(thing_card_lines) // 8)] # Adaptively organizes the lines so that they can be formatted and printed (formula)
    # Loop that prints all of the ascii cards with spaces and indents in between as well  as numbers and everything else
    for i in range(8):
        print(' ' * 4, end='')
        for j in range(len(thing_card_lines) // 8):
            print(thing_card_lines[j * 8 + i].ljust(max_lengths[j] + 2), end='')
        print()

# DEALING CARDS -------------------------------------------------------------------------------
    
# Function to deal cards to players and opponents
def dealingCards():
    global contestedDict, playerCards, opponentCards, deck

    # Creates deck depending on numDecks
    deck = []
    for _ in range(numDecks):
        deck.extend((rank, suit) for suit in suits for rank in ranks)
    random.shuffle(deck)

    # Reset cards
    opponentCards = {}
    # Deal player 1 cards
    playerCards = [deck.pop() for _ in range(2)]


    # Dynamically create dictionary keys and values for each opponent, and then deal cards
    # WARNING: To understand this code, you need to realise that each opponent is set to a value, which is the range of number of players
    # The player is set to 0 naturally
    # Every dictionary and list that references the player or opponents naturally will assign them with ther given key
    # Meaning for EVERY dictionary referencing opponents, opponent #3 (if it exists) will be assigned to the key value --> 3:X
    # I will comment out every dictionary that uses this play assignment method

    for i in range(1, numPlayers + 1):
        key = str(f'opponent{i}')
        value = [deck.pop() for _ in range(2)]
        opponentCards[key] = value

    # Contested Dict is a dictionary with (player:worth) of their hand
    contestedDict = {}


# COMPARING CARDS -------------------------------------------------------------------------------

# Find the total hand of a player
def handRanking(card1, card2, player):
    
    # Creates rankSet list (basically the player's available hand including the table's hand)
    rankSet = [numRank(card1[0]), numRank(card2[0])]
    rankSet.extend([numRank(t[0]) for t in tableCards])  # funny how I made rankSet a list, not a set, too lazy to change now

    # Creates suitSet list
    suitSet = [card1[1], card2[1]]
    suitSet.extend([t[1] for t in tableCards])

    # Convert the deck into a new variable
    sortedRankSet = sorted(rankSet)

    # Find occurences of ranks
    rank_counts = {} # Dictionary in form of rank:ocurrences
    for rank in rankSet:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    rankOccurences = list(rank_counts.values())

    # Find occurences of suits
    suit_counts = {} # Dictionary in form of suit:ocurrences
    for suit in suitSet:
        suit_counts[suit] = suit_counts.get(suit, 0) + 1
    suitOccurrences = list(suit_counts.values())


    # Royal Flush
    if set(rankSet) == {'10', '11', '12', '13', '14'} and suitOccurrences.count(5) >= 1: # If rankSet values are inside {'10', '11', '12', '13', '14'} and all suits are same then you're the lucky winner
        contestedDict[player] = 10
        return 'Royal Flush'
        
    # Straight Flush
    elif all(sortedRankSet[i + 1] - sortedRankSet[i] == 1 for i in range(len(sortedRankSet)-1)) and suitOccurrences.count(5) >= 1: # Same as Straight, but also checks if all 5 cards are the same suit
        contestedDict[player] = 9
        return 'Straight Flush'
    
    # Four of a Kind
    elif rankOccurences.count(4) == 1: # Looks into the values of rank_counts dictionary and finds if a pair of 4 exists.
        contestedDict[player] = 8
        return 'Four of a Kind'
    
    # Full House
    elif rankOccurences.count(3) == 1 and rankOccurences.count(2) == 1: # Looks into the values of rank_counts dictionary and finds if a pair of 3 of the same rank and a pair of 2 exists.
        contestedDict[player] = 7
        return 'Full House'
    
    # Flush
    elif suitOccurrences.count(5) >= 1: # Looks into the values of suit_counts dictionary and finds if a pair of 5 of the same suits exists.
        contestedDict[player] = 6
        return 'Flush'
    
    # Straight
    elif all(sortedRankSet[i + 1] - sortedRankSet[i] ==  1 for i in range(len(sortedRankSet)-1)) and len(rankSet) >= 5: # Subtracts a card value from the next one when sorted, if they equal to 1, its a straight
        contestedDict[player] = 5
        return 'Straight'
    
    # Three of a kind
    elif rankOccurences.count(3) == 1: # Looks into the values of rank_counts dictionary and finds if a pair of 3 of the same rank exists.
        contestedDict[player] = 4
        return 'Three of a kind'
    
    # Two pair
    elif rankOccurences.count(2) == 2: # Looks into the values of rank_counts dictionary and finds if 2 pairs exists.
        contestedDict[player] = 3
        return 'Two Pair'
    
    # Pair
    elif rankOccurences.count(2) == 1: # Looks into the values of rank_counts dictionary and finds if a pair exists.
        contestedDict[player] = 2
        return 'Pair'
    
    # High Card  
    else:
        contestedDict[player] = 1
        return 'High Card'
    

# BETTING MECHANICS -------------------------------------------------------------------------------------------------------

pot = 0 # Setup pot

playerCash = {}
for i in range(0, numPlayers+1):
    playerCash[i] = 500 # Set player cash

# Function to add cash to the pot and subtract it from player
def potAdd(playerKey, quantity):
    global pot
    playerCash[playerKey] -= quantity
    pot += quantity

# Function to add cash to the player and subtract it from the pot
def potSubtract(playerKey):
    global pot
    playerCash[playerKey] += pot
    pot = 0

# Function to evenly add cash to the players when there is a tie and subtract it from the pot
def potSubtractOnTie(playerList):
    global pot
    quantityToAdd = int(pot / len(playerList))
    for winningPlayer in playerList:
        playerCash[winningPlayer] += quantityToAdd
    pot = 0
    
# plBetPos, or playerBettingPosition is a dictionary in the setup of (player:bettingRole), betting role is what determines when each player bets
plBetPos = {}

# Minimum bet amount

# Asks player for their bet with limitations, and redifines MIN_BET
def get_player_bet(player_key, available_cash):
    while True:
        try:
            print(f"{Fore.GREEN}You have {available_cash} cash. Enter your bet (minimum {MIN_BET}): {Fore.RESET}", end='', flush=True)
            bet = int(input())
            if bet < MIN_BET or bet > available_cash:
                print(f"Invalid bet. Minimum bet is {MIN_BET}, and you cannot bet more than your available cash.")
            else:
                return bet
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_opponent_bet(playerCashAmount):
    if MIN_BET >= playerCashAmount:
        return playerCashAmount
    else:
        return int(MIN_BET * random.uniform(1.0, 1.5))

def betting():
    global MIN_BET
    for i in range(0, numPlayers + 1):
        if i == 0:
            bet = get_player_bet(i, playerCash[0])
            MIN_BET = bet
        else:
            bet = get_opponent_bet(playerCash[i])
            MIN_BET = bet

        potAdd(i, bet)
        textPlayer = 'Opponent ' + str(i) if i != 0 else 'You'
        print(f"{textPlayer} bet {bet}.")
        time.sleep(1)


def bettingPosition(iteration):
    global plBetPos
    for i in range(0, numPlayers + 1):
        position = 'Dealer' if i == iteration % numPlayers else \
                   'Small Blind' if (i - 1) % numPlayers == iteration % numPlayers else \
                   'Big Blind' if (i - 2) % numPlayers == iteration % numPlayers else i

        plBetPos[i] = position



# PRINT ALL (VISUAL) -------------------------------------------------------------------------------


# Print all function that prints the screen with clear
def printAll(tableState=0):
    def blankCard(quantity):
        return [('?', '?') for _ in range(quantity)]

    # Start by setting table cards to blank so visuals can update at the same time
    global tableCards
    tableCards = []

    tableWord='?'

    # Table cards print and print Player Cards
    for _ in range(4):
        print("\033c", end="")

        print("\nTable: " + tableWord)

        
        # Table Flop
        if tableState == 1:
            tableCards = [deck.pop() for _ in range(3)]
            tempTableCards = copy.deepcopy(tableCards)
            # Deals table cards which also sets for rest of if statements
            tempTableCards.extend(blankCard(2))
            ASCIIPrintFormat(tempTableCards) # Function calling the ASCII format function, but with the blank cards as well
            tableWord = 'Turn'
        # Table Turn
        elif tableState == 2:
            tempTableCards.pop(-1)
            tempTableCards.pop(-1)
            poppedCard = deck.pop()
            tableCards.append(poppedCard)
            tempTableCards.append(poppedCard)
            tempTableCards.extend(blankCard(1))
            ASCIIPrintFormat(tempTableCards)
            tableWord = 'River'
        # Table River
        elif tableState == 3:
            tempTableCards.pop(-1)
            poppedCard = deck.pop()
            tableCards.append(poppedCard)
            tempTableCards.append(poppedCard)
            ASCIIPrintFormat(tempTableCards)
            tableWord = ''
        else:
            ASCIIPrintFormat(blankCard(5))
            tableWord = 'Flop'
        tableState += 1

        print() # New Line

        print(f'{Fore.GREEN}Pot: {pot}\n{Fore.RESET}')

        # Print Player Cards
        print(str() + Fore.BLUE + 'Player' + str(' (') + str(playerCash[0]) + ' Cash)' + Fore.RESET + (f'{Fore.LIGHTYELLOW_EX} - {str(plBetPos[0])}{Fore.RESET}' if isinstance(plBetPos[0], str) else '')) # Prints all player data
        # Printing Handranking
        print(f'{Fore.LIGHTBLUE_EX}{handRanking(*playerCards, 0)}:{Fore.RESET}')
        
        ASCIIPrintFormat(playerCards)
        print() # New Lin


       # Print Opponent Cards
        for i in range(1, numPlayers+1): # Loop that calls opponent dictionary and finds card values, and prints all data
            opponent = opponentCards[f'opponent{i}']
            print(Fore.LIGHTRED_EX + 'Opponent ' +  str(i) + ' (' + str(playerCash[i]) +' Cash)' + Fore.RESET + (f'{Fore.LIGHTYELLOW_EX} - {str(plBetPos[i])}{Fore.RESET}' if isinstance(plBetPos[i], str) else ''))
            # Printing Handranking
            print(f'{Fore.LIGHTRED_EX}{handRanking(opponent[0], opponent[1], i)}:{Fore.RESET}')
            
            # same thing as top but for opponents
            ASCIIPrintFormat(opponent)
            print() # New Line
        betting() # Calling betting funciton
        time.sleep(1)


# FINDING WINNER -------------------------------------------------------------------------------
        
def findingWinner():
    # Iterate through all values in contestedDict, and if it is the same value as max_value, add it to a new dictionary
    winningPlayers = {player: value for player, value in contestedDict.items() if value == max(contestedDict.values())}

    # Output the winner if theres only one
    if len(winningPlayers) == 1:
        winner_index = next(iter(winningPlayers.keys()))
        if winner_index == 0:
            winner = f'{Fore.GREEN}The winner is: Player!{Fore.RESET}'
            potSubtract(0)
        else:
            winner = f'{Fore.GREEN}The winner is: Opponent {winner_index}!{Fore.RESET}'
            potSubtract(winner_index)

    # Complicated sentence structure if there's a tie
    else:
        potSubtractOnTie(winningPlayers.keys())
        winners = [f'Player' if i == 0 else f'Opponent {i}' for i in winningPlayers.keys()]
        winners_str = ', '.join(winners[:-1]) + ' and ' + winners[-1]
        winner = f'Tie! The winners are: {winners_str}!'

    # Prints basically who won
    print(winner)


# RESETING GAME -------------------------------------------------------------------------------

def is_one_player_remaining():
    net_worth_values = list(playerCash.values())
    
    # Check if the maximum value is greater than 0
    if max(net_worth_values) > 0:
        # Check if there is only one player with a non-zero balance
        return net_worth_values.count(0) == len(net_worth_values) - 1
    else:
        # All players have 0 cash
        return False


# Loops the game so that same players can remain the same but just resets card and money
loopIteration = 0
while True:
    # Reset Betting
    MIN_BET = 10
    
    dealingCards()
    bettingPosition(loopIteration)
    printAll()
    findingWinner()
    input("Press Enter to continue...")
    loopIteration += 1
    print("\033c", end="")
    NetWorth = [i for i in  playerCash.Values()]
    if is_one_player_remaining():
        print('GAME OVER')
        break