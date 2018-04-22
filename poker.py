
'''
Created on Mar 11, 2018

@author: Spencer
'''
import card
import code

def read_holdem_hand(hole_cards, board_cards):
    '''read holdem hand. 21 combination of 5 cards. current implementation is an exhaustive approach; 
       checks every possible combination of 5 card hands and evaluates the hand, keeping track of the
       largest hand found. returns the "code" of the best possible hand'''
    cards = []
    
    board_card_1 = [0,0,0,0,0,0,1,1,1,2]
    board_card_2 = [1,1,1,2,2,3,2,2,3,3]
    board_card_3 = [2,3,4,3,4,4,3,4,4,4]
    
    highest_code = [-1]
    
    #using both hole cards, same baord card options as omaha
    for bci in range(len(board_card_1)):
        cards.append(hole_cards[0])
        cards.append(hole_cards[1])
        
        cards.append(board_cards[board_card_1[bci]])
        cards.append(board_cards[board_card_2[bci]])
        cards.append(board_cards[board_card_3[bci]])
        
        code = read_hand(cards, highest_code[0])        
        
        if code[0] != -1 and compare_codes(code, highest_code) == 1:
            highest_code = code
            
        cards.clear()
    
    #using only one card from hand, 4 from board    
    board_card_1 = [0,0,0,0,1]
    board_card_2 = [1,1,1,2,2]
    board_card_3 = [2,2,3,3,3]
    board_card_4 = [3,4,4,4,4]
        
    for bci in range(len(board_card_1)):
        cards.append(hole_cards[0])
        
        cards.append(board_cards[board_card_1[bci]])
        cards.append(board_cards[board_card_2[bci]])
        cards.append(board_cards[board_card_3[bci]])
        cards.append(board_cards[board_card_4[bci]])

        code = read_hand(cards, highest_code[0])        
        
        if code[0] != -1 and compare_codes(code, highest_code) == 1:
            highest_code = code
            
        cards.clear()
        
    for bci in range(len(board_card_1)):
        cards.append(hole_cards[1])
        
        cards.append(board_cards[board_card_1[bci]])
        cards.append(board_cards[board_card_2[bci]])
        cards.append(board_cards[board_card_3[bci]])
        cards.append(board_cards[board_card_4[bci]])

        code = read_hand(cards, highest_code[0])        
        
        if code[0] != -1 and compare_codes(code, highest_code) == 1:
            highest_code = code
            
        cards.clear()
    
    #playing board    
    for c in board_cards:
        cards.append(c)
        
    code = read_hand(cards, highest_code[0])        
        
    if code[0] != -1 and compare_codes(code, highest_code) == 1:
        highest_code = code
        
    return highest_code     
    
def compare_lows(low_list_1, low_list_2):
    '''ascending = - (<) , descending = + (>), congruent with java compareTo(). NOTE!: assumes both lists are exactly 5 elements long
       AND sorted in DESCENDING order'''
    
    for i in range(5):
        #if 1 is lower than 2
        if low_list_1[i] < low_list_2[i]:
            return -1
        #if 2 is lower than 1
        elif low_list_1[i] > low_list_2[i]:
            return 1
        
    return 0


def read_omaha_low(hole_cards, board_cards, big_omaha = False):
    '''read omaha low hand. returns a descending list of exactly 5 integers, no repeats, representing low. if no low possible, returns 
       a list with exactly one element [-1]  '''
    
    if big_omaha:
        hole_card_1 = [0,0,0,0,1,1,1,2,2,3]
        hole_card_2 = [1,2,3,4,2,3,4,3,4,4]
        
    else:
        hole_card_1 = [0,0,0,1,1,2]
        hole_card_2 = [1,2,3,2,3,3]
    
    board_card_1 = [0,0,0,0,0,0,1,1,1,2]
    board_card_2 = [1,1,1,2,2,3,2,2,3,3]
    board_card_3 = [2,3,4,3,4,4,3,4,4,4]
    
    lowest = [-1]
    
    cards = []
    
    for hci in range(len(hole_card_1)):
        hc = []
        hc.append(hole_cards[hole_card_1[hci]])
        hc.append(hole_cards[hole_card_2[hci]])
        
        for bci in range(board_card_1.__len__()):
            bc = []
            bc.append(board_cards[board_card_1[bci]])
            bc.append(board_cards[board_card_2[bci]])
            bc.append(board_cards[board_card_3[bci]])
            
            cards.clear()
            
            for h in hc:
                cards.append(h)
                
            for b in bc:
                cards.append(b)
                
            cards = sort_cards(cards)
            
            low = []
            
            #leaves us with a sorted (descending) list of integer ranks, no repeats
            for c in cards:
                if low.count(c.return_rank()) == 0:
                    low.append(c.return_rank())
            
            #if the list is less than 5 items long, low not possible, exit now before wasting resources
            if len(low) < 5:
                continue
            
            #if the first element is an ace (there should be at most one occurrence, remove it and add a 1 to the end of the list      
            if low[0] == 14:
                low.remove(14)
                low.append(1)
            
            #sorts in ascending
            low.sort()
            
            #splices the first five, leaving us with the lowest 5
            low = low[:5]
            
            #sort in descending
            low.sort(reverse = True)
            
            #appropriately assigns 'lowest'
            if lowest[0] == -1 or compare_lows(lowest, low) == 1:
                lowest = low
    
    #if qualifying low (8 or lower)
    if lowest[0] <= 8:
        return lowest
    
    #non-qualifying low
    return [-1]
    
    
def read_omaha_hand(hole_cards, board_cards, big_omaha = False):
    '''read omaha hand, same way as holdem hand. check all 60 combinations 
    of using 2 from your hand, 3 from the board'''
    
    if big_omaha:
        hole_card_1 = [0,0,0,0,1,1,1,2,2,3]
        hole_card_2 = [1,2,3,4,2,3,4,3,4,4]
        
    else:
        hole_card_1 = [0,0,0,1,1,2]
        hole_card_2 = [1,2,3,2,3,3]
    
    board_card_1 = [0,0,0,0,0,0,1,1,1,2]
    board_card_2 = [1,1,1,2,2,3,2,2,3,3]
    board_card_3 = [2,3,4,3,4,4,3,4,4,4]
    
    highest_code = [-1]
    highest_hci = 0
    highest_bci = 0
    cards = []
    
    for hci in range(hole_card_1.__len__()):
        hc = []
        hc.append(hole_cards[hole_card_1[hci]])
        hc.append(hole_cards[hole_card_2[hci]])
        
        for bci in range(board_card_1.__len__()):
            bc = []
            bc.append(board_cards[board_card_1[bci]])
            bc.append(board_cards[board_card_2[bci]])
            bc.append(board_cards[board_card_3[bci]])
            
            cards.clear()
            
            for h in hc:
                cards.append(h)
                
            for b in bc:
                cards.append(b)
            
            code = read_hand(cards, highest_code[0])
            
            if code[0] != -1 and compare_codes(code, highest_code) == 1:
                highest_code = code
                highest_bci = bci
                highest_hci = hci
    
    return highest_code

    
def sort_cards(unsorted):
    '''sorts cards based on rank only, descending order'''
    sorted = []
    
    while unsorted:
        largest = unsorted[0]
        for card in unsorted:
            if card.return_rank() > largest.return_rank():
                largest = card
        
        sorted.append(largest)
        unsorted.remove(largest)
    return sorted

            
def read_hand(cards, lower_limit = 0):
    '''read a poker hand. will search for hands >= to lower limit. will not search for hands lower
       than lower limit parameter. if searching is ended prematurely due to the lower limit parameter, 
       a list containing -1 will be returned. the "cards" parameter expects a list of exactly 5 card instances'''
        
    cards = sort_cards(cards) #sort cards first, descending order based on rank
    
    code = check_for_straight_flush(cards)
    if code[0] == 9:
        return code
    
    #if we dont need to check for any hands lower than straight flush
    if lower_limit == 9:
        return [-1]
    
    code = check_for_quads(cards)
    if code[0] == 8:
        return code
    
    #if we dont need to check for any hands lower than quads
    if lower_limit == 8:
        return [-1]
    
    code = check_for_full_house(cards)
    if code[0] == 7:
        return code
   
    #if we dont need to check for any hands lower than full house    
    if lower_limit == 7:
        return [-1]
    
    code = check_for_flush(cards)
    if code[0] == 6:
        return code
    
    #if we dont need to sheck for any hands lower than flush
    if lower_limit == 6:
        return [-1]
    
    code = check_for_straight(cards)
    if code[0] == 5:
        return code    
    
    #if we don't need to check for any hands lower than straight
    if lower_limit == 5:
        return [-1]
    
    code = check_for_trips(cards)
    if code[0] == 4:
        return code
    
    #if we don't need to check for any hands lower than trips
    if lower_limit == 4:
        return [-1]
    
    code = check_for_two_pair(cards)
    if code[0] == 3:
        return code
    
    #if we don't need to check for any hands lower than 2 pair
    if lower_limit == 3:
        return [-1]

    code = check_for_pair(cards)
    if code[0] == 2:
        return code
    
    #if we don't need to check for any hands lower than 1 pair
    if lower_limit == 2:
        return [-1]
    
    #if we get here, the hand is 'high card'
    code.clear()
    code.append(1) #code for high card
    
    for c in cards:
        code.append(c.return_rank()) #value of high card
    
    return code
    
    
def check_for_pair(cards):
    '''check for pair. assume bigger hands have already been caught. 5 element code'''
    rank_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    code = [0]
        
    for c in cards:
        rank_count[c.return_rank() - 2] += 1
        
    r = 12
    while r >= 0:
        if rank_count[r] == 2: #we have found our pair
            code.clear()
            code.append(2) #code for a single pair
            code.append(r + 2) #rank of pair
            
            k = 12
            while k >= 0: #should never reach terminating condition
                if rank_count[k] == 1: #we have found kicker1
                    code.append(k + 2) #value of kicker1
                    
                    l = k - 1
                    while l >= 0: #should never reach terminating condition
                        if rank_count[l] == 1: #we have found kicker2
                            code.append(l + 2) #value of kicker2
                            
                            m = l - 1
                            while m >= 0: #should never reach terminating condition
                                if rank_count[m] == 1: #we have found kicker3
                                    code.append(m + 2) #value of kicker3
                                    return code
                                m -= 1
                        l -= 1
                k -= 1
        r -= 1
                            
    return [0] #not a 1pair hand
            
            
def check_for_two_pair(cards):
    '''check for two pair. assume bigger hands have already been caught. 4 element code'''
    rank_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    code = [0]
        
    for c in cards:
        rank_count[c.return_rank() - 2] += 1
        
    r = 12
    while r >= 1:
        if rank_count[r] == 2: # we have pair number 1
            c = r - 1
            while c >= 0:
                if rank_count[c] == 2: # we have pair number 2
                    code.clear()
                    code.append(3) # code for 2 pair
                    code.append(r + 2) #rank of larger pair
                    code.append(c + 2) #rank of smaller pair
                    
                    k = 12
                    while k >= 0: #loop should never reach terminating condition as there should always be a kicker
                        if rank_count[k] == 1: #we have found our kicker
                            code.append(k + 2) #value of kicker
                            return code
                        k -= 1
                c -= 1
        r -= 1                
    return [0]       

def check_for_trips(cards):
    '''check for trips. assuming that full houses have already been caught. 4 element code'''
    rank_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    code = [0]
    
    for c in cards:
        rank_count[c.return_rank() - 2] += 1
        
    for t in range(len(rank_count)):
        if rank_count[t] == 3: #we have trips
            code.clear()
            code.append(4) #code for trips
            code.append(t + 2) #rank of trips
            
            k1 = 12
            while k1 > -1:
                if rank_count[k1] == 1: #we have kicker number 1
                    code.append(k1 + 2) #kicker1 value
                    
                    k2 = k1 - 1
                    while k2 > -1: #this loop should actually never reach terminating condition since there should always be a 2nd kicker
                        if rank_count[k2] == 1: #we have kicker number 2
                            code.append(k2 + 2) #kicker2 value
                            return code
                        k2 -= 1
                k1 -= 1
    return [0] #no trips

def check_for_full_house(cards):
    '''check for full house, 3 element code, FH, trips rank, pair rank'''
    code = [0]
    
    rank_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    for c in cards:
        rank_count[c.return_rank() - 2] += 1
        
    for r in range(len(rank_count)):
        if rank_count[r] == 3: # we have trips
            for p in range(len(rank_count)):
                if rank_count[p] == 2: # we have a pair, thus, FH
                    code.clear()
                    code.append(7) #code for full house
                    code.append(r + 2) #rank of trips
                    code.append(p + 2) #rank of pair
                    return code
        
    return [0] 

def check_for_quads(cards):
    '''checking for 4 of a kind, 3 element code. quads, quads rank, kicker rank'''
    code = [0]
    
    rank_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    for c in cards:
        rank_count[c.return_rank() - 2] += 1
        
    for r in range(len(rank_count)):
        if rank_count[r] == 4: # we have quads
            code.clear()
            code.append(8) #code for quads
            code.append(r + 2) #rank of quads
            
            for r in range(len(rank_count)):
                if rank_count[r] == 1: #we have found the kicker
                    code.append(r + 2)
                    return code
                        
    return [0] #no quqds

def check_for_straight_flush(cards):
    '''check for straight flush. 2 element code, straight flush code plus the highest straight flush card'''
    
    code = check_for_straight(cards)
    
    if code[0] == 5: #we have a straight
        code = check_for_flush(cards)
        
        if code[0] == 6: # we have a flush
            code.clear()
            code.append(9) #code for straight flush
            
            if cards[0].return_rank() != 14: #not a straight flush containing an ace
                code.append(cards[0].return_rank()) #highest card of the straigt flush (for comparison purposes)
                return code
                
            elif cards[0].return_rank() == 14: #can be a 5 high SF or ace high SF, need to discern
                if cards[1].return_rank() == 13: #ace high SF
                    code.append(13)
                    return code
                
                elif cards[1].return_rank() == 5: #5 high SF
                    code.append(5)
                    return code

    return [0] #not a straight flush

def check_for_flush(cards):
    '''check for flush, 6-element code, flush plus 5 ranked cards'''
    code = [0]
    
    suit_count = [0, 0, 0, 0]
    
    for c in cards:
        suit_count[c.return_suit()-1] += 1
        
    for s in suit_count:
        if s == 5:
            # we have a flush
            code.clear()
            code.append(6) #code for flush
            
            # this adds the ranks of the flush cards in descending order (for comparison purposes)
            for c in cards:
                code.append(c.return_rank())
                
            return code
        
    return [0] #not a flush

def hand_to_string(code):
    '''depict the code of the hand to a string representing the hand'''
    title = ''
    if code[0] == 1:
        title = card.rank_to_string(code[1]) + " high"
        
    elif code[0] == 2:
        title = "Pair of " + card.rank_to_string(code[1]) + "s"
    
    elif code[0] == 3:
        title = "Two pair, " + card.rank_to_string(code[1]) + "s"
        title = title + " and " + card.rank_to_string(code[2]) + "s"
    
    elif code[0] == 4:
        title = "Three of a kind " + card.rank_to_string(code[1]) + "s"
    
    elif code[0] == 5:
        title = "Straight, " + card.rank_to_string(code[1]) + " high"
    
    elif code[0] == 6:
        title = "Flush, " + card.rank_to_string(code[1]) + " high"
    
    elif code[0] == 7:
        title = "Full house, " + card.rank_to_string(code[1]) + "s"
        title = title + " over " + card.rank_to_string(code[2]) + "s"
    
    elif code[0] == 8:
        title = "Quad " + card.rank_to_string(code[1]) + "s"
    
    elif code[0] == 9:
        title = "Straight flush, " + card.rank_to_string(code[1]) + " high"
    
    return title    

def compare_codes(code_1, code_2):
    '''ascending = - (<) , descending = + (>), congruent with java compareTo()'''
    i = 0
    while i < len(code_1) and i < len(code_2):
        if code_1[i] > code_2[i]:
            return 1
        elif code_1[i] < code_2[i]:
            return -1
        i += 1
    return 0

def compare_hands(hole_cards_1, hole_cards_2, board_cards, game_type = 'texas'):
    '''ascending = -, descending = +, congruent with java compareTo()'''
    
    code_1 = read_hand(hole_cards_1, board_cards)
    code_2 = read_hand(hole_cards_2, board_cards)
    
    i = 0
    while i < len(code_1) and i < len(code_2):
        if code_1[i] > code_2[i]:
            return 1
        elif code_1[i] < code_2[i]:
            return -1
        i += 1
    return 0

def check_for_straight(cards):
    '''check for straight. 2-element code. straight plus high card'''
    code = [0]
    
    #NOTE!!! assuming cards are already sorted (descending based on rank)
    #checking for non-wheel straight
    if cards[0].return_rank() - cards[1].return_rank() == 1:
        if cards[1].return_rank() - cards[2].return_rank() == 1:
            if cards[2].return_rank() - cards[3].return_rank() == 1:
                if cards[3].return_rank() - cards[4].return_rank() == 1:
                    #we have a straight
                    code.clear()
                    code.append(5)
                    code.append(cards[0].return_rank())
                    
                    return code
                
    #checking for wheel
    if cards[0].return_rank() == 14:
        if cards[1].return_rank() == 5:
            if cards[2].return_rank() == 4:
                if cards[3].return_rank() == 3:
                    if cards[4].return_rank() == 2:
                        code.clear()
                        code.append(5) #code for straight
                        code.append(5) #signifying that the straight is 5-high
                        
                        return code

    return [0] #not a straight
    
    