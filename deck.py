'''
Created on Mar 10, 2018

@author: Spencer
'''
from card import Card
from random import randint

class Deck():
    '''class representing a deck of Cards'''
    
    def __init__(self, deck_type = 'full_suited'):
        '''initializer, deck type to create'''
        self.deck = []
        self.initialize(deck_type)
        
    def initialize(self, deck_type = 'full_suited'):
        '''initialize the deck depending on deck_type'''
        
        #if deck should be full and suited (Default case)
        if deck_type == 'full_suited':
            self.deck.clear()
            for suit in range(1, 5):
                self.deck.append(Card(14, suit))
                for rank in range(2, 14):
                    self.deck.append(Card(rank, suit))
                
    def print_deck(self):
        '''print the deck in formatted form'''
        for card in self.deck:
            print(card.return_string())
            
    def shuffle_deck(self):
        '''shuffle the deck'''
        shuffled_deck = []
        
        while len(self.deck) > 0:
            shuffled_deck.append(self.deck.pop(randint(0, len(self.deck) - 1)))
        
        self.deck = shuffled_deck
    
    def pop(self, index=0):
        '''pop (retrieve and remove from deck) card at index index'''
        return self.deck.pop(index)
    
    def push(self, card_list):
        '''push list of cards on to top of deck,
           ***note, first card in list pushed first'''
        for card in card_list:
            self.deck.insert(0, card)
        