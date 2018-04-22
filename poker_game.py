'''
Created on Mar 11, 2018

@author: Spencer
'''

from deck import Deck
import poker

class PokerGame():
    '''class to represent a game of poker. holds deck, players, etc'''

    def __init__(self, game_type = 'texas'):
        '''initializer, sets game type'''
        self.game_type = game_type
        self.player_list = []
        self.deck = Deck()
        self.board_cards = []
        
    def add_player(self, player):
        '''add a player to the player list at the table'''
        self.player_list.append(player)

    def reveal_all(self):
        '''testing, reveal everything, determine and reveal winning hand'''
        winners = [self.player_list[0]]
        
        for player in self.player_list:
            print(player.get_name())
            hand = player.show_hand()
            print(poker.hand_to_string(poker.read_hand(hand, self.board_cards)))
            
            if poker.compare_hands(winners[0].show_hand(), hand, self.board_cards) == -1:
                winners = [player]
                
            elif poker.compare_hands(winners[0].show_hand(), hand, self.board_cards) == 0:
                winners.append(player)
            
            for card in hand:
                print(card.return_string())       
                 
        print("Board cards:")
        for card in self.board_cards:
            print(card.return_string())    
            
        for player in winners:
            string = "Winner is " + player.get_name() + " with a "
            string += poker.hand_to_string(poker.read_hand(player.show_hand(), self.board_cards))
            print(string)
    
    def get_game_type(self):
        return self.game_type
    
    def get_board(self):
        return self.board_cards        
    
    def deal_hand(self, game_type = 'texas'):
        '''deal the appropriate cards'''
        
        self.game_type = game_type
        self.deck.shuffle_deck()
        
        if self.game_type == 'texas':
            for c in range(0,2):
                for player in self.player_list:
                    player.get_dealt_card(self.deck.pop())
                    
            for c in range(0,5):
                self.board_cards.append(self.deck.pop())
        
        
    