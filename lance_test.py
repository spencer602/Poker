'''
Created on Apr 18, 2018

@author: Spencer
'''

import poker
import deck
import card

lance = 0.0
jonny = 0.0

for i in range(100000000):
    pot = 2.0
    
    lance -= 1.0
    jonny -= 1.0
    
    this_deck = deck.Deck()

    big_o_hand = []
    ace_deuce_hand = []
    board_cards = []
    
    ace_deuce_hand.append(this_deck.pop())
    ace_deuce_hand.append(this_deck.pop())
    
    this_deck.shuffle_deck()
    
    ace_deuce_hand.append(this_deck.pop())
    ace_deuce_hand.append(this_deck.pop())
    
    for l in range(5):
        big_o_hand.append(this_deck.pop())
    
    for l in range(5):
        board_cards.append(this_deck.pop())
        
    big_o_low = poker.read_omaha_low(big_o_hand, board_cards, big_omaha = True)
    ace_deuce_low = poker.read_omaha_low(ace_deuce_hand, board_cards)
    big_o_code = poker.read_omaha_hand(big_o_hand, board_cards, big_omaha = True)
    ace_deuce_code = poker.read_omaha_hand(ace_deuce_hand, board_cards)
    
    #bigO has no low, aceDeuce has low
    if big_o_low[0] == -1 and ace_deuce_low[0] != -1:
        lance += 1.0
        pot = 1.0
    
    #bigO has low, aceDeuce has no low
    elif big_o_low[0] != -1 and ace_deuce_low[0] == -1:
        jonny += 1.0
        pot = 1.0
    
    #both have low
    elif big_o_low[0] != -1 and ace_deuce_low[0] != -1:
        #bigO low is better
        if poker.compare_lows(big_o_low, ace_deuce_low) == -1:
            jonny += 1.0
        #aceDeuce low is lower   
        elif poker.compare_lows(big_o_low, ace_deuce_low) == 1:
            lance += 1.0
        #low is tie  
        elif poker.compare_lows(big_o_low, ace_deuce_low) == 0:
            lance += .5
            jonny += .5
        pot = 1.0
    
    #aceDeuce hand is better    
    if poker.compare_codes(big_o_code, ace_deuce_code) == -1:
        lance += pot
    #bigO hand is better
    elif poker.compare_codes(big_o_code, ace_deuce_code) == 1:
        jonny += pot
    
    #tie
    elif poker.compare_codes(big_o_code, ace_deuce_code) == 0:
        jonny += pot/2
        lance += pot/2
        
    if i % 100 == 0:
        print(str(i))
        print("Lance: " + str(lance))
        print("Jonny: " + str(jonny))
        print()
        


        
        
            



