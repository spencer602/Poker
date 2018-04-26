'''
Created on Apr 20, 2018 (blaze it)

@author: Peter
'''

from deck import Deck
from card import Card
from collections import Counter
import numpy


boardCards = []
playerCards = []


'''This first block of methods all set up the board to be read'''
def print_cards(cards):
    output = ""
    for i in range(0, len(cards)):
        output = output + cards[i].return_rank_char() + cards[i].return_suit_char() + " "
    print(output)


def deal_cards(deck, cards, who):
    '''Deals 5 cards from a deck'''
    for j in range(0, cards):
        who.append(deck.pop())


def get_ranks(board):
    '''Returns the rank of the cards as an array'''
    boardRanks = []
    for k in range(0, len(board)):
        boardRanks.append(board[k].return_rank())
    return boardRanks


def get_suits(board):
    '''Returns the suit of the cards as an array'''
    boardSuits = []
    for l in range(0, len(board)):
        boardSuits.append(board[l].return_suit_char())
    return boardSuits


def get_card_pairs(cards):
    '''Returns a list of card pairs that can be made from a 4 card omaha hand'''
    card_pairs = []
    for i in range(0, len(cards)):
        for j in range(i+1,len(cards)):
            card_pairs.append((cards[i], cards[j]))
    return card_pairs


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

    if(mostCommonSuit>=3):
        #print("Flush is possible")
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
    for i in range(0, len(sorted)-2):
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
        print("quads is possible")
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
                if card_pair_comparison(i,j):
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

        '''Get card pairs from the player's hand that are of the correct suit'''
        hand_pairs = get_card_pairs(hand)
        suited_hand_pairs = []
        for i in hand_pairs:
            if i[0].return_suit() == i[1].return_suit() == flush_suit:
                suited_hand_pairs.append(i)

        '''Return the card pairs that match possible straight flush card pairs'''
        for i in suited_hand_pairs:
            for j in sf_cards:
                if card_pair_comparison(i, j):
                    straight_flushes.append(i)

    return straight_flushes


def find_quads(board, hand):
    '''Returns a list of card pairs that make quads'''
    possibleQuads = []

    '''Get the ranks of the board cards, and how often they appear'''
    board_ranks = get_ranks(board)
    counts = Counter(board_ranks).most_common(2)
    most_common_board_rank = counts[0][0]
    most_appears_board = counts[0][1]
    second_common_board_rank = counts[1][0]
    second_appears_board = counts[1][1]

    sorted = list(reversed(numpy.unique(board_ranks)))

    card_pairs = get_card_pairs(hand)

    if most_appears_board == 1:
        return possibleQuads
    elif most_appears_board == 2 or second_appears_board == 2:
        for i in card_pairs:
            if i[0].return_rank() == i[1].return_rank() == most_common_board_rank:
                possibleQuads.append(i)
            elif i[0].return_rank() == i[1].return_rank() == second_common_board_rank and second_appears_board == 2:
                possibleQuads.append(i)
    elif most_appears_board == 3 and second_appears_board == 1:
        for i in card_pairs:
            if i[0].return_rank() == most_common_board_rank or i[1].return_rank() == most_common_board_rank:
                possibleQuads.append(i)
    elif most_appears_board == 3 and second_appears_board == 2:
        for i in card_pairs:
            if i[0].return_rank() == most_common_board_rank or i[1].return_rank() == most_common_board_rank or i[0].return_rank() == i[1].return_rank() == second_common_board_rank:
                possibleQuads.append(i)
    elif most_appears_board >=4:
        return possibleQuads

    return possibleQuads


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

    if counts[0][1] == 2:
        for i in card_pairs:
            if i[0].return_rank() == counts[0][0] and i[1].return_rank() in board_ranks:
                boat_cards.append(i)
            elif i[1].return_rank() == counts[0][0] and i[0].return_rank() in board_ranks:
                boat_cards.append(i)
            elif i[1].return_rank() == i[0].return_rank() and i[0].return_rank() in board_ranks:
                boat_cards.append(i)
        return boat_cards
    elif counts[0][1] >= 3:
        for i in card_pairs:
            if i[1].return_rank() == i[0].return_rank():
                boat_cards.append(i)
        return boat_cards
    else:
        return boat_cards


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

    '''A flush is only possible if there is at least 3 of one suit on the board.'''
    if count_on_board >= 3:
        flush_possible = True
    else:
        return flush_cards

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
            return hand_flush_cards
        elif len(hand_flush_cards) > 2:
            '''Get the biggest 2 flush cards'''
            flush_ranks = get_ranks(hand_flush_cards)
            sorted = list(reversed(numpy.unique(flush_ranks)))
            flush_pair = []
            for i in range(0, len(hand_flush_cards)):
                if hand_flush_cards[i].return_rank() == sorted[0] or hand_flush_cards[i].return_rank() == sorted[1]:
                    flush_pair.append(hand_flush_cards[i])

            flush_cards = flush_pair
    return flush_cards


def find_straights(board, hand):
    '''Returns a list of card pairs that make a straight'''
    possibleStraights = []

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
                theNuts = (sorted[i] + 2, sorted[i] + 1)
                theDumbEnd = (sorted[i] - 3, sorted[i] - 4)
                theMiddle = (sorted[i] + 1, sorted[i] - 3)
                possibleStraights.append(theNuts)
                possibleStraights.append(theDumbEnd)
                possibleStraights.append(theMiddle)
            elif diff_one == 1 and diff_two == 3:
                possibleStraights.append((sorted[i] - 2, sorted[i] - 4))
                possibleStraights.append((sorted[i] + 1, sorted[i] - 2))
            elif diff_one == 1 and diff_two == 4:
                possibleStraights.append((sorted[i] - 2, sorted[i] - 3))
            elif diff_one == 2 and diff_two == 3:
                possibleStraights.append((sorted[i] - 1, sorted[i] - 4))
            elif diff_one == 2 and diff_two == 4:
                possibleStraights.append((sorted[i] - 1, sorted[i] - 3))
            elif diff_one == 3 and diff_two == 4:
                possibleStraights.append((sorted[i] - 1, sorted[i] - 2))

    '''The algorithm above includes cards that don't exist. For example on a KQJ board,
    it would give (15,14) as an option. The loop below deletes elements that contain non-
    existent cards.'''
    straights = []
    for i in range(0,len(possibleStraights)):
        if  0 < possibleStraights[i][0] <= 14 and 0 < possibleStraights[i][1] <= 14:
            straights.append(possibleStraights[i])

    hand_pairs = get_card_pairs(hand)
    straights_in_hand = []
    for j in straights:
        for i in hand_pairs:
            if (i[0].return_rank() == j[0] and i[1].return_rank() == j[1]) or (i[0].return_rank() == j[1] and i[1].return_rank() == j[0]):
                straights_in_hand.append(i)

    return set(straights_in_hand)


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

def find_pairs(board):
    '''Returns a list of card pairs that make pairs'''


def best_hand(board, hand):
    '''Returns the best two cards to play'''
    if len(find_straight_flushes(board,hand)) > 0:
        return find_straight_flushes(board, hand)
    elif len(find_quads(board, hand)) > 0:
        return find_quads(board, hand)
    elif len(find_flushes(board, hand)) > 0:
        return find_flushes(board, hand)
    elif len(find_straights(board, hand)) > 0:
        return find_straights(board, hand)

n = 1000
for i in range(0, n):
    boardCards = []
    playerCards = []
    aDeck = Deck()
    aDeck.shuffle_deck()
    deal_cards(aDeck, 5, boardCards)
    deal_cards(aDeck, 4, playerCards)
    results = list(find_trips(boardCards, playerCards))
    if len(results) >= 1:
        print_cards(boardCards)
        print_cards(playerCards)
        for i in results:
            print_cards(list(i))
        print("////////////")


'''boardCards = [Card(9, 3), Card(2, 4), Card(5, 3), Card(5, 1), Card(10, 1)]
playerCards = [Card(9, 4), Card(9, 2), Card(5, 2), Card(4, 3)]
print_cards(boardCards)
print_cards(playerCards)
results = find_quads(boardCards,playerCards)
for i in results:
    print_cards(i)'''




