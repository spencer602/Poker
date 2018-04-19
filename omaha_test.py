'''
Created on Apr 17, 2018

@author: Spencer
'''

import deck
import card
import poker

poker_deck = deck.Deck()

control_hand = []
random_hand = []
board_cards = []

control_hand.append(poker_deck.pop())
control_hand.append(poker_deck.pop())

poker_deck.shuffle_deck()

control_hand.append(poker_deck.pop())
control_hand.append(poker_deck.pop())

for i in range(4):
    random_hand.append(poker_deck.pop())
    
for i in range(5):
    board_cards.append(poker_deck.pop())

print("Control hand:")

for c in control_hand:
    print(c.return_string())
    
print("\nRandom hand:")    

for c in random_hand:
    print(c.return_string())
    
print("\nBoard Cards:")

for c in board_cards:
    print(c.return_string())
    
control_hand_code = poker.read_omaha_hand(control_hand, board_cards)
low = poker.read_omaha_low(control_hand, board_cards)

print("\nControl hand: " + poker.hand_to_string(control_hand_code))
print ("Low: " + str(low))

    







