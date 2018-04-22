'''
Created on Mar 11, 2018

@author: Spencer
'''

from deck import Deck
from card import Card
import poker

deck = Deck()

total_tries = 0

hand_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]

while True:
    total_tries += 1
    deck.shuffle_deck()
    hole_cards = []
    board_cards = []
    
    for r in range(0,2):
        hole_cards.append(deck.pop())
    
    for r in range(0,5):
        board_cards.append(deck.pop())
    
    hand_count[poker.read_holdem_hand(hole_cards, board_cards)[0] - 1] += 1
    
    print("Hand #: " + str(total_tries) + " " + str(hand_count))
    
    deck.push(hole_cards)
    deck.push(board_cards)
    
    

