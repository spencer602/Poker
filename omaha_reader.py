'''
Created on Apr 20, 2018 (blaze it)

@author: Peter
'''

from deck import Deck
from collections import Counter
import numpy


boardCards = []
boardRanks = []
boardSuits = []

def print_board(board):
    for i in board:
        print(i.return_string())

def deal_board(deck):
    '''Deals 5 cards from a deck'''
    for j in range(0, 5):
        boardCards.append(deck.pop())

def get_ranks():
    '''Assigns the rank of the cards to an array'''
    for j in range(0, 5):
        boardRanks.append(boardCards[j].return_rank())

def get_suits():
    '''Assigns the suit of the cards to an array'''
    for j in range(0, 5):
        boardSuits.append(boardCards[j].return_suit_string())

def check_flush(board):
    '''Returns TRUE if a flush is possible on a given board'''
    flush = False
    counts = Counter(board)

    mostCommonSuit = counts.most_common(1)[0][1]

    if(mostCommonSuit>=3):
        flush = True

    return flush

def check_straight(board):
    '''Returns TRUE if a straight is possible on a given board'''
    sorted = list(reversed(numpy.unique(board)))
    print(sorted)

    if (sorted[0] == 14):
        sorted.append(1)
        print("Aces are high and low")
        print(sorted)


def check_quads(board):
    '''Returns TRUE if quads is possible on a given board'''

'''Test run below:'''
aDeck = Deck()
aDeck.shuffle_deck()
deal_board(aDeck)
print_board(boardCards)
get_ranks()
get_suits()

if check_flush(boardSuits):
    print("Flush is possible")
else:
    print("Flush is not possible")

check_straight(boardRanks)


