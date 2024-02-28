import random
import time
import os

os.system('clear')
input('''
---------------------------------------------------
 ____  _            _    __  __          __   __
|  _ \| |          | |  |  \/  |   /\    \ \ / /
| |_) | | __ _  ___| | _| \  / |  /  \    \ V / 
|  _ <| |/ _` |/ __| |/ / |\/| | / /\ \    > <  
| |_) | | (_| | (__|   <| |  | |/ ____ \  / . \ 
|____/|_|\__,_|\___|_|\_\_|  |_/_/    \_\/_/ \_\ \n
---------------------------------------------------
     WELCOME TO MAX'S BLACKJACK SIMULATOR
              Press Enter to Start ''')

while True:
    # Defining Cards
    suits = ['♥', '♦', '♠', '♣']
    numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = [(number, suit) for suit in suits for number in numbers]
    
    # Shuffle deck and deal to the player and dealer
    random.shuffle(deck)
    player_cards = []
    dealer_cards = []
    player_value = 0
    dealer_value = 0

    # Create and adjust ascii card into a function
    def card(number, suit):
        if len(number) == 1:

            # Single-digit number
            line1 = f'┌─────────┐ '
            line2 = f'│ {number}{suit}      │ '.format(number, suit)
            line3 = f'│         │ '
            line4 = f'│         │ '
            line5 = f'│         │ '
            line6 = f'│         │ '
            line7 = f'│      {number}{suit} │ '.format(number, suit)
            line8 = f'└─────────┘ '

        else:
            # Double-digit number
            line1 = f'┌─────────┐ '
            line2 = f'│ {number}{suit}     │ '.format(number, suit)
            line3 = f'│         │ '
            line4 = f'│         │ '
            line5 = f'│         │ '
            line6 = f'│         │ '
            line7 = f'│     {number}{suit} │ '.format(number, suit)
            line8 = f'└─────────┘ '

        # Pad shorter lines with spaces to ensure all lines have the same length
        lines = [line1, line2, line3, line4, line5, line6, line7, line8]
        return lines

    # Switching value of J Q K A to its actual value
    def card_value(card):
        if card[0] in ['J', 'Q', 'K']:
            return 10
        elif card[0] == 'A':
            return 11
        else:
            return int(card[0])

    # Hit function
    def hit(player, num=1):
        global player_value, dealer_value, newCard
        for _ in range(num):
            newCard = deck.pop()
            cards, value = (player_cards, player_value) if player == 'player' else (dealer_cards, dealer_value)
            cards.append(newCard)
            value += card_value(newCard)
            num_aces = cards.count(('A',))
            while value > 21 and num_aces:
                value -= 10
                num_aces -= 1

            # Update the global variable
            if player == 'player':
                player_value = value
            else:
                dealer_value = value

    # Count and return cards of dealer and player
    def cardCount(player=False):
        global player_value, dealer_value
        result_list = []

        if player:
            totalCards = player_cards
        else:
            totalCards = dealer_cards

        for card_info in totalCards:
            lines = card(card_info[0], card_info[1])
            result_list.extend(lines)

        return result_list

    
    # Print all of dealer and players cards
    def cardPrint():
        print("\033c", end="")

        # Print dealer cards and calling cardCount()
        print(f'Dealer has a total of {dealer_value}:\n')
        dealer_card_lines = cardCount()
        max_lengths = [max(len(line) for line in dealer_card_lines[i * 8:(i + 1) * 8]) for i in range(len(dealer_card_lines) // 8)]
        for i in range(8):
            for j in range(len(dealer_card_lines) // 8):
                print(dealer_card_lines[j * 8 + i].ljust(max_lengths[j] + 2), end=' ')
            print()

        # Print player cards and calling cardCount()
        print(f'\nPlayer has a total of {player_value}:\n')
        player_card_lines = cardCount(True)
        max_lengths = [max(len(line) for line in player_card_lines[i * 8:(i + 1) * 8]) for i in range(len(player_card_lines) // 8)]
        for i in range(8):
            for j in range(len(player_card_lines) // 8):
                print(player_card_lines[j * 8 + i].ljust(max_lengths[j] + 2), end=' ')
            print()

    hit('player', 2)
    hit('dealer', 2)
    # Print Cards
    time.sleep(1)
    cardPrint()
    
    # Ask for input and save it to variable
    hitStand = input('Do you want to hit or stand? \n')

    # Player game loop
    while True:
        # Hit
        if hitStand.title() == 'Hit':
            hit('player', 1)

            # Hit if else
            if player_value > 21:
                print(f'Bust! Your total is {player_value}. You lose')
                break
            else:
                cardPrint()
                hitStand = input('\nDo you want to hit or stand?\n')

        # Stand
        elif hitStand.title() == 'Stand':
            print(f'You chose to stand. Your final total value is {player_value}')

            # Dealer play loop
            while dealer_value <= player_value:
                if dealer_value < 17:
                    hit('dealer', 1)
                    time.sleep(1)
                    cardPrint()
                    time.sleep(1)
                # Chec if dealer or player wins on dealer stand
                if dealer_value > 21:
                    print(f'Dealer Bust! The dealer\'s total is {dealer_value}. You win')
                    break
                elif dealer_value >= 17:
                    print(f'Dealer decided to stand. The dealer\'s total is {dealer_value}')
                    if dealer_value == player_value:
                        print('You have tied with the dealer!')
                        break
                    elif dealer_value > player_value:
                        print('Dealer wins!')
                        break
                    else:
                        print('You win!')
                        break
            break
        else:
            input('That\'s not a valid option. Press Enter and try again.\n')
            hitStand = input('Do you want to hit or stand?\n')

    time.sleep(1)
    input("Press enter to play again")
    print("\033c", end="")