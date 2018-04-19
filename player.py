'''
Created on Mar 11, 2018

@author: Spencer
'''
from card import Card
import poker

class Player():
    '''class to represent a card player. has his own hands'''
    
    def __init__(self, name, poker_game):
        '''initializer including name'''
        self.name = name
        self.hand = []
        self.poker_game = poker_game
        
    def get_name(self):
        '''returns the name of the player'''
        return self.name
    
    def get_dealt_card(self, card):
        '''recieve a card into hand'''
        self.hand.append(card)
        
    def read_hand(self):
        '''figure out what hand you have'''
        hand = poker.read_hand(self.hand, self.poker_game.get_board(), self.poker_game.get_game_type())
        print(hand)
        
    def show_hand(self):
        '''return the hand to the game'''
        return self.hand