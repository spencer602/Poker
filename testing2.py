'''
Created on Mar 12, 2018

@author: Spencer
'''

import poker

from deck import Deck
from card import Card

deck = Deck()
deck.shuffle_deck()

cards = []

for a in range(0,10):
    cards.append(deck.pop())

for card in cards:
    print(card.return_string())

cards = poker.sort_cards(cards)
print()

for card in cards:
    print(card.return_string())
