'''
Created on Apr 20, 2018 (blaze it)

@author: Peter
'''

from deck import Deck
from card import Card
from collections import Counter
import numpy
import poker
import itertools

'''This first block of methods all set up the board to be read'''


def print_cards(cards):
    output = ""
    for i in list(cards):
        output = output + i.return_rank_char() + i.return_suit_char() + " "
    print(output)


def deal_cards(deck, cards, who):
    '''Deals 5 cards from a deck'''
    for j in range(0, cards):
        who.append(deck.pop())


def get_ranks(board):
    '''Returns the rank of the cards as a list'''
    boardRanks = []
    for k in range(0, len(board)):
        boardRanks.append(board[k].return_rank())
    return boardRanks


def get_suits(board):
    '''Returns the suit of the cards as a list'''
    boardSuits = []
    for l in range(0, len(board)):
        boardSuits.append(board[l].return_suit_char())
    return boardSuits


def get_card_pairs(cards):
    '''Returns a list of card pairs that can be made from a 4 card omaha hand'''
    card_pairs = []
    for i in range(0, len(cards)):
        for j in range(i + 1, len(cards)):
            card_pairs.append([cards[i], cards[j]])
    return card_pairs


def get_subsets(cards, n):
    '''Returns a list of all subsets of "cards" with n elements'''
    return list(itertools.combinations(cards, n))


def card_pair_comparison(cardsA, cardsB):
    '''Returns true if two pairs of cards are identical'''
    same = False

    if cardsA[0] == cardsB[0] or cardsA[0] == cardsB[1]:
        if cardsA[1] == cardsB[0] or cardsA[1] == cardsB[1]:
            same = True
            return same

    return same


'''This block of methods determine if a class of hand is possible on a given board'''


def check_flush(board):
    '''Returns TRUE if a flush is possible on a given board'''
    board = get_suits(board)
    flush = False
    counts = Counter(board)

    mostCommonSuit = counts.most_common(1)[0][1]

    if (mostCommonSuit >= 3):
        # print("Flush is possible")
        flush = True

    return flush


def check_straight(board):
    '''Returns TRUE if a straight is possible on a given board'''
    board = get_ranks(board)
    straight = False

    '''Sorts the board by rank from highest (14) to lowest (2)'''
    sorted = list(reversed(numpy.unique(board)))

    '''If there are less than three unique cards on the board there is no straight possible'''
    if len(sorted) < 3:
        return straight

    '''Aces are high and low, and simply adding another card to the board
     to represent the low ace (1) won't have an effect on how the board is read'''
    if sorted[0] == 14:
        sorted.append(1)

    '''Since the list is sorted, we can just examine pairs of cards that have a card between them,
    (e.g. 1st and 3rd) and check their difference. If it's less than 5 we know a straight is possible.'''
    for i in range(0, len(sorted) - 2):
        diff_one = sorted[i] - sorted[i + 1]
        diff_two = sorted[i] - sorted[i + 2]
        if diff_two < 5:
            straight = True
            break
    return straight


def check_quads(board):
    '''Returns TRUE if quads is possible on a given board'''
    board = get_ranks(board)
    quads = False
    sorted = list(reversed(numpy.unique(board)))

    '''If there are less than 5 unique cards, it is a paired board'''
    if len(sorted) < 5:
        quads = True
        return quads
    else:
        return quads


def check_straight_flush(board, hand):
    '''Finds all the possible straight flush card pairs on a given board'''
    sf_cards = []
    straight_flushes = []
    '''First check to see if both a straight and a flush are possible'''
    if check_flush(board) and check_straight(board):
        sf_possibility = []
        '''Determine which suit the potential straight flush will be'''
        suits = get_suits(board)
        counts = Counter(suits)
        flush_suit = counts.most_common(1)[0][0]
        '''Add each card of that suit to the list of possible straight flush cards'''
        for card in board:
            if card.return_suit_char() == flush_suit:
                sf_possibility.append(card)

        '''Get the ranks of all the suited cards, and sort in descending order'''
        ranks = list(reversed(numpy.unique(get_ranks(sf_possibility))))

        '''Make sure cards are properly initialized'''
        if flush_suit == 's':
            flush_suit = 1
        elif flush_suit == 'h':
            flush_suit = 2
        elif flush_suit == 'd':
            flush_suit = 3
        elif flush_suit == 'c':
            flush_suit = 4

        '''Find the possible straights given the suited cards'''
        straights = find_straights(sf_possibility)
        for i in straights:
            sf_cards.append((Card(i[0], flush_suit), Card(i[1], flush_suit)))

        hand_pairs = get_card_pairs(hand)
        suited_hand_pairs = []
        for i in hand_pairs:
            if i[0].return_suit() == i[1].return_suit() == flush_suit:
                suited_hand_pairs.append(i)

        for i in suited_hand_pairs:
            for j in sf_cards:
                if card_pair_comparison(i, j):
                    straight_flushes.append(i)

    return straight_flushes


def check_low(board):
    '''Returns TRUE if a low is possible on a given board'''
    board = get_ranks(board)
    low = False
    sorted = list(reversed(numpy.unique(board)))

    if sorted[0] == 14:
        sorted.append(1)

    lowCards = [num for num in sorted if num < 9]

    if len(lowCards) >= 3:
        low = True
        return low
    else:
        return low


'''Methods to determine the best possible hand now that we know what hands are possible'''


def find_straight_flushes(board, hand):
    '''Returns a list of card pairs that make a straight flush, or null if there are none
    Ideally this list will be sorted by strongest to weakest hand'''
    '''Finds all the possible straight flush card pairs on a given board'''
    sf_cards = []
    straight_flushes = []
    '''First check to see if both a straight and a flush are possible'''
    if check_flush(board) and check_straight(board):
        sf_possibility = []
        '''Determine which suit the potential straight flush will be'''
        suits = get_suits(board)
        counts = Counter(suits).most_common()
        flush_suit = counts[0][0]
        '''Add each card of that suit to the list of possible straight flush cards'''
        for card in board:
            if card.return_suit_char() == flush_suit:
                sf_possibility.append(card)

        '''Make sure cards are properly initialized'''
        if flush_suit == 's':
            flush_suit = 1
        elif flush_suit == 'h':
            flush_suit = 2
        elif flush_suit == 'd':
            flush_suit = 3
        elif flush_suit == 'c':
            flush_suit = 4

        '''Get card pairs from the player's hand that are of the correct suit'''
        suited_hand_cards = []
        for i in hand:
            if i.return_suit() == flush_suit:
                suited_hand_cards.append(i)

        '''Find the possible straights given the suited cards'''
        straight_flushes = find_straights(sf_possibility, suited_hand_cards)
        if straight_flushes == [0]:
            return [0]
        else:
            return [9, straight_flushes[1][0]]
    else:
        return [0]


def find_quads(board, hand):
    '''Returns a list of card pairs that make quads'''
    possibleQuads = []
    '''Get the ranks of the board cards, and how often they appear'''
    board_ranks = get_ranks(board)
    hand_ranks = get_ranks(hand)
    counts = Counter(board_ranks).most_common(2)
    most_common_board_rank = counts[0][0]
    most_appears_board = counts[0][1]
    second_common_board_rank = counts[1][0]
    second_appears_board = counts[1][1]

    sorted = list(reversed(numpy.unique(board_ranks)))

    card_pairs = get_card_pairs(hand)

    if most_appears_board == 1:  #Unpaired board, no quads possible
        return [0]
    elif (most_appears_board == 2 or second_appears_board == 2) and not set(board_ranks).isdisjoint(set(hand_ranks)):  #Single or double paired board
        for i in card_pairs:
            if i[0].return_rank() == i[1].return_rank() == most_common_board_rank:
                non_quads = [x for x in sorted if x != most_common_board_rank]
                for j in board:
                    if j.return_rank() == most_common_board_rank:
                        i.append(j)
                    elif j.return_rank() == non_quads[0]:
                        i.append(j)
                    del i[5:]
                    possibleQuads.append(i)
            elif i[0].return_rank() == i[1].return_rank() == second_common_board_rank and second_appears_board == 2:
                non_quads = [x for x in sorted if x != second_common_board_rank]
                for j in board:
                    if j.return_rank() == second_common_board_rank:
                        i.append(j)
                    elif j.return_rank() == non_quads[0]:
                        i.append(j)
                del i[5:]
                possibleQuads.append(i)
    elif most_appears_board == 3 and second_appears_board == 1 and not set(board_ranks).isdisjoint(set(hand_ranks)):  #Tripled board
        for i in card_pairs:
            if i[0].return_rank() == most_common_board_rank or i[1].return_rank() == most_common_board_rank:
                non_quads = [x for x in sorted if x != most_common_board_rank]
                for j in board:
                    if j.return_rank() == most_common_board_rank:
                        i.append(j)
                for j in board:
                    if j.return_rank() == non_quads[0] and len(i) < 5:
                        i.append(j)
                possibleQuads.append(i)
    elif most_appears_board == 3 and second_appears_board == 2 and not set(board_ranks).isdisjoint(set(hand_ranks)):  #Full house on board
        for i in card_pairs:
            if i[0].return_rank() == most_common_board_rank or i[1].return_rank() == most_common_board_rank:
                non_quads = [x for x in sorted if x != most_common_board_rank]
                for j in board:
                    if j.return_rank() == most_common_board_rank:
                        i.append(j)
                for j in board:
                    if j.return_rank() == non_quads[0] and len(i) < 5:
                        i.append(j)
                possibleQuads.append(i)
            elif i[0].return_rank() == i[1].return_rank() == second_common_board_rank:
                non_quads = [x for x in sorted if x != second_common_board_rank]
                for j in board:
                    if j.return_rank() == second_common_board_rank:
                        i.append(j)
                for j in board:
                    if j.return_rank() == non_quads[0] and len(i) < 5:
                        i.append(j)
                possibleQuads.append(i)
    elif most_appears_board >= 4:  #Quads on board, no quads possible
        return [0]

    largest = 0

    for i in range(0, len(possibleQuads)):
        code = ''
        for j in poker.check_for_quads(possibleQuads[i]):
            code += str(j)
        if int(code) > largest:
            largest = int(code)
            possibleQuads.insert(0, possibleQuads.pop(i))
    del possibleQuads[1:]

    if len(possibleQuads) > 0:
        return poker.check_for_quads(possibleQuads[0])
    else:
        return [0]


def find_boats(board, hand):
    '''Returns a list of card pairs that make a full house'''
    boat_cards = []
    board_ranks = get_ranks(board)
    counts = Counter(board_ranks).most_common()
    ''' modal rank of the board = counts[0][0]
           how often it appears = counts[0][1]
    2nd modal rank of the board = counts[1][0]
           how often it appears = counts[1][1]'''
    card_pairs = get_card_pairs(hand)

    if counts[0][1] == 2:  #Paired board
        for i in card_pairs:
            if i[0].return_rank() == counts[0][0] and i[1].return_rank() in board_ranks:  #Trips + another pair
                for j in board:
                    if j.return_rank() == i[0].return_rank() or j.return_rank() == i[1].return_rank():
                        i.append(j)
                boat_cards.append(i)
            elif i[1].return_rank() == counts[0][0] and i[0].return_rank() in board_ranks:  #Trips + another pair
                for j in board:
                    if j.return_rank() == i[0].return_rank() or j.return_rank() == i[1].return_rank():
                        i.append(j)
                boat_cards.append(i)
            elif i[1].return_rank() == i[0].return_rank() and i[0].return_rank() in board_ranks:  #Set + paired board
                if counts[1][1] == 1:  #single paired board
                    for j in board:
                        if j.return_rank() == i[0].return_rank() or j.return_rank() == i[1].return_rank():
                            i.append(j)
                        if j.return_rank() == counts[0][0]:
                            i.append(j)
                    boat_cards.append(i)
                elif counts[1][1] == 2:  #double paired board
                    pairs = [counts[0][0], counts[1][0]]
                    for k in pairs:
                        hole_cards = i[:]
                        for j in board:
                            if j.return_rank() == k or j.return_rank() == i[0].return_rank():
                                hole_cards.append(j)
                        boat_cards.append(hole_cards)
    elif counts[0][1] >= 3:  #Tripled board
        for i in card_pairs:
            if i[1].return_rank() == i[0].return_rank():  #pocket pair
                for j in board:
                    if j.return_rank() == counts[0][0]:
                        i.append(j)
                boat_cards.append(i)

    largest = 0

    for i in range(0, len(boat_cards)):
        code = ''
        for j in poker.check_for_full_house(boat_cards[i]):
            code += str(j)
        if int(code) > largest:
            largest = int(code)
            boat_cards.insert(0, boat_cards.pop(i))
    del boat_cards[1:]

    if len(boat_cards) > 0:
        return poker.check_for_full_house(boat_cards[0])
    else:
        return [0]


def find_flushes(board, hand):
    '''Returns a list of card pairs that make a flush'''
    flush_cards = []
    flush_possible = False

    '''Info about the suit of the board cards'''
    board_suits = get_suits(board)
    '''Creates a counter that gives us the most commonly occurring suit, and how often it appears'''
    board_counts = Counter(board_suits)
    '''Which suit:'''
    flush_suit = board_counts.most_common(1)[0][0]
    '''How often:'''
    count_on_board = board_counts.most_common(1)[0][1]

    board_flush_cards = []
    for j in board:
        if j.return_suit_char() == flush_suit:
            board_flush_cards.append(j)
    board_ranks = get_ranks(board_flush_cards)
    sorted = list(reversed(numpy.unique(board_ranks)))
    del sorted[3:]


    '''A flush is only possible if there is at least 3 of one suit on the board.'''
    if count_on_board >= 3:
        flush_possible = True
    else:
        return [0]

    '''This portion of the code only executes if a flush is possible given the board'''
    if flush_possible:

        '''List of flush cards in a given hand'''
        hand_flush_cards = []

        '''Adds cards to this list if they match the flush suit on the board'''
        for i in hand:
            if i.return_suit_char() == flush_suit:
                hand_flush_cards.append(i)

        '''If this list has length = 2, only one flush is possible with the hand.
        If there are more than 2 cards, then the best flush is the biggest 2.'''
        if len(hand_flush_cards) == 2:
            for j in board:
                if j.return_suit_char() == flush_suit and j.return_rank() in sorted:
                    hand_flush_cards.append(j)
            flush_cards = hand_flush_cards
        elif len(hand_flush_cards) > 2:
            '''Get the biggest 2 flush cards'''
            flush_ranks = get_ranks(hand_flush_cards)
            sorted_hand = list(reversed(numpy.unique(flush_ranks)))
            flush_pair = []
            for i in range(0, len(hand_flush_cards)):
                if hand_flush_cards[i].return_rank() == sorted_hand[0] or hand_flush_cards[i].return_rank() == sorted_hand[1]:
                    flush_pair.append(hand_flush_cards[i])
            for j in board:
                if j.return_suit_char() == flush_suit and j.return_rank() in sorted:
                    flush_pair.append(j)
            flush_cards = flush_pair
    return poker.check_for_flush(flush_cards)


def find_straights(board, hand):
    '''Returns a list of card pairs that make a straight'''
    possibleStraights = []
    card_pairs = []

    '''Gets the ranks, sorts the board, and adds the low ace exactly like check_straight()'''
    board = get_ranks(board)
    sorted = list(reversed(numpy.unique(board)))
    if sorted[0] == 14:
        sorted.append(1)

    for i in range(0, len(sorted) - 2):
        diff_one = sorted[i] - sorted[i + 1]
        diff_two = sorted[i] - sorted[i + 2]

        if diff_two < 5:
            if diff_one == 1 and diff_two == 2:
                possibleStraights.append((sorted[i] + 2, sorted[i] + 1, sorted[i], sorted[i] - 1, sorted[i] - 2))
                possibleStraights.append((sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3, sorted[i] - 4))
                possibleStraights.append((sorted[i] + 1, sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3))
                card_pairs.append((sorted[i] + 2, sorted[i] + 1))
                card_pairs.append((sorted[i] - 3, sorted[i] - 4))
                card_pairs.append((sorted[i] + 1, sorted[i] - 3))
            elif diff_one == 1 and diff_two == 3:
                possibleStraights.append((sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3, sorted[i] - 4))
                possibleStraights.append((sorted[i] + 1, sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3))
                card_pairs.append((sorted[i] - 2, sorted[i] - 4))
                card_pairs.append((sorted[i] + 1, sorted[i] - 2))
            elif diff_one == 1 and diff_two == 4:
                possibleStraights.append((sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3, sorted[i] - 4))
                card_pairs.append((sorted[i] - 2, sorted[i] - 3))
            elif diff_one == 2 and diff_two == 3:
                possibleStraights.append((sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3, sorted[i] - 4))
                possibleStraights.append((sorted[i] + 1, sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3))
                card_pairs.append((sorted[i] - 1, sorted[i] - 4))
                card_pairs.append((sorted[i] + 1, sorted[i] - 1))
            elif diff_one == 2 and diff_two == 4:
                possibleStraights.append((sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3, sorted[i] - 4))
                card_pairs.append((sorted[i] - 1, sorted[i] - 3))
            elif diff_one == 3 and diff_two == 4:
                possibleStraights.append((sorted[i], sorted[i] - 1, sorted[i] - 2, sorted[i] - 3, sorted[i] - 4))
                card_pairs.append((sorted[i] - 1, sorted[i] - 2))

    '''The algorithm above includes cards that don't exist. For example on a KQJ board,
    it would give (15,14) as an option. The loop below deletes elements that contain non-
    existent cards.'''
    straights = []
    hole_cards = []
    for i in range(0, len(possibleStraights)):
        if possibleStraights[i][0] <= 14:
            straights.append(possibleStraights[i])
            hole_cards.append(card_pairs[i])

    hand_pairs = get_card_pairs(hand)
    made_straight = []
    for j in range(0, len(straights)):
        for i in hand_pairs:
            if (i[0].return_rank() == hole_cards[j][0] and i[1].return_rank() == hole_cards[j][1]) \
                    or (i[0].return_rank() == hole_cards[j][1] and i[1].return_rank() == hole_cards[j][0]):
                made_straight.append(straights[j])

    if len(made_straight) > 0:
        largest = 0
        for i in range(1, len(made_straight)):
            if made_straight[i][0] > made_straight[largest][0]:
                largest = i
        made_straight.insert(0, made_straight.pop(largest))
        return [5, made_straight[0][0]]

    return [0]


def find_trips(board, hand):
    '''Returns a list of card pairs that make trips'''
    trips_cards = []
    board_ranks = get_ranks(board)
    counts = Counter(board_ranks).most_common()
    ''' modal rank of the board = counts[0][0]
           how often it appears = counts[0][1]
    2nd modal rank of the board = counts[1][0]
           how often it appears = counts[1][1]'''
    card_pairs = get_card_pairs(hand)

    if counts[0][1] == 1:
        for i in card_pairs:
            if i[1].return_rank() == i[0].return_rank() and i[0].return_rank() in board_ranks:
                trips_cards.append(i)
    elif counts[0][1] == 2:
        for i in card_pairs:
            if i[0].return_rank() == counts[0][0] or i[1].return_rank() == counts[0][0]:
                trips_cards.append(i)
            elif counts[1][1] == 2:
                if i[0].return_rank() == counts[1][0] or i[1].return_rank() == counts[1][0]:
                    trips_cards.append(i)
    elif counts[0][1] == 3:
        for i in card_pairs:
            trips_cards.append(i)

    return trips_cards


def find_smaller_hands(board, hand):
    board_triplets = get_subsets(board, 3)
    hand_pairs = get_subsets(hand, 2)
    highest_code = [0]
    for i in board_triplets:
        for j in hand_pairs:
            five_card = i + j
            five_card_ranks = get_ranks(five_card)
            sorted = list(reversed(numpy.unique(five_card_ranks)))
            if len(poker.check_for_trips(five_card)) > 1:
                this_code = poker.check_for_trips(five_card)
            elif len(poker.check_for_two_pair(five_card)) > 1:
                this_code = poker.check_for_two_pair(five_card)
            elif len(poker.check_for_pair(five_card)) > 1:
                this_code = poker.check_for_pair(five_card)
            else:
                this_code = [1, sorted[0]]
            if poker.compare_codes(highest_code, this_code) < 0:
                highest_code = this_code

    return poker.hand_to_string(highest_code)


def best_hand(board, hand):
    if len(find_straight_flushes(board, hand)) > 1:
        return poker.hand_to_string(find_straight_flushes(board, hand))
    elif len(find_quads(board, hand)) > 1:
        return poker.hand_to_string(find_quads(board, hand))
    elif len(find_boats(board, hand)) > 1:
        return poker.hand_to_string(find_boats(board, hand))
    elif len(find_flushes(board, hand)) > 1:
        return poker.hand_to_string(find_flushes(board, hand))
    elif len(find_straights(board, hand)) > 1:
        return poker.hand_to_string(find_straights(board, hand))
    else:
        return find_smaller_hands(board, hand)

def test_run(n):
    for i in range(0, n):
        boardCards = []
        playerCards = []
        aDeck = Deck()
        aDeck.shuffle_deck()
        deal_cards(aDeck, 5, boardCards)
        deal_cards(aDeck, 4, playerCards)
        print_cards(boardCards)
        print_cards(playerCards)
        print(best_hand(boardCards, playerCards))
        print("////////////")


'''Use test_run to deal out n random boards and hands. As of right now, the different methods have
slightly different return types, so you may have to tweak the parameter you give to print_cards()'''
test_run(1)

'''boardCards = []
aDeck = Deck()
aDeck.shuffle_deck()
deal_cards(aDeck, 5, boardCards)
results = get_subsets(boardCards, 3)
for i in results:
    print_cards(i)'''


'''Use the code below to debug a specific situation'''
'''
boardCards = [Card(12, 4), Card(6, 4), Card(11, 4), Card(10, 2), Card(13, 2)]
playerCards = [Card(14, 3), Card(5, 2), Card(8, 4), Card(10, 4)]
print_cards(boardCards)
print_cards(playerCards)
results = best_hand(boardCards, playerCards)
print(results)

4c Ah 5h 8c 2s 
4s 3d Ad Jc 
Two pair, Aces and Fours
'''


