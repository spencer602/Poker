'''
Created on Mar 11, 2018

@author: Spencer
'''


from player import Player
from poker_game import PokerGame

player_names = ['Spencer', 'Todd', 'Dasha', 'Professor', 'Pete', 'Stew', 'Monkey', 'CDK']
game = PokerGame()

for player in player_names:
    game.add_player(Player(player, game))
    
game.deal_hand()

game.reveal_all()

