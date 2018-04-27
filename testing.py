'''
Created on Mar 11, 2018

@author: Spencer
'''

from deck import Deck
import poker
import time

deck = Deck()

total_tries = 0

TOTAL_DISTINCT = 133784560
frequency = [23294460, 58627800, 31433400, 6461620, 6180020, 4047644, 3473184, 224848, 41584]

for i in range(9):
    frequency[i] = frequency[i] / TOTAL_DISTINCT
    
hand_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
expected = [0,0,0,0,0,0,0,0,0]

percentage_error = [0,0,0,0,0,0,0,0,0]
initial_time = time.time()
start_time = time.time()

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
    
    if total_tries % 10000 == 0:
        for i in range(9):
            expected[i] = frequency[i] * total_tries
            percentage_error[i] = round((hand_count[i] - expected[i]) / expected[i] * 100, 3)
            
        print("Hand #: " + str(round(total_tries/1000)) + "k   time: " + str(round(time.time() - start_time, 3))  + 
              "   total time: " + str(round(time.time() - initial_time, 3)) + "   " + str(percentage_error))
        start_time = time.time()
    
    deck.push(hole_cards)
    deck.push(board_cards)
    
    

