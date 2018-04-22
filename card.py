'''
Created on Mar 10, 2018

@author: Spencer
'''

class Card():
    '''class representing individual cards'''
    
    def __init__(self, rank, suit):
        '''initializer, rank and suit are integers'''
        self.rank = rank
        self.suit = suit
        self.title = ''
        self.suit_title = ''
        self.rank_title = ''
        
        self.initialize()
    
    def return_rank(self):
        '''returns rank as integer'''
        return self.rank
        
    def return_rank_string(self):
        '''returns rank as string'''
        return self.rank_title
        
    def return_suit(self):
        '''returns suit at integer, 1=spades, 2=hearts, 3=diamonds
           4=clubs'''
        return self.suit
    
    def return_suit_string(self):
        '''returns suit as string'''
        return self.suit_title
        
    def return_suit_char(self):
        '''returns suit as a letter'''
        if self.suit == 1:
            return 's'
        elif self.suit == 2:
            return 'h'
        elif self.suit == 3:
            return 'd'
        elif self.suit == 4:
            return 'c'

    def return_rank_char(self):
        if self.rank == 2:
            return '2'
        elif self.rank == 3:
            return '3'
        elif self.rank == 4:
            return '4'
        elif self.rank == 5:
            return '5'
        elif self.rank == 6:
            return '6'
        elif self.rank == 7:
            return '7'
        elif self.rank == 8:
            return '8'
        elif self.rank == 9:
            return '9'
        elif self.rank == 10:
            return 'T'
        elif self.rank == 11:
            return 'J'
        elif self.rank == 12:
            return 'Q'
        elif self.rank == 13:
            return 'K'
        elif self.rank == 14:
            return 'A'

    def return_string(self):
        ''' returns card as formatted string ex: Ace of Spades'''
        return self.title
    
    def initialize_rank(self):
        '''initialize rank of cards, rank_title as string'''
        if self.rank == 2:
            self.rank_title = 'Two'
        elif self.rank == 3:
            self.rank_title = 'Three'
        elif self.rank == 4:
            self.rank_title = 'Four'
        elif self.rank == 5:
            self.rank_title = 'Five'
        elif self.rank == 6:
            self.rank_title = 'Six'
        elif self.rank == 7:
            self.rank_title = 'Seven'
        elif self.rank == 8:
            self.rank_title = 'Eight'
        elif self.rank == 9:
            self.rank_title = 'Nine'
        elif self.rank == 10:
            self.rank_title = 'Ten'
        elif self.rank == 11:
            self.rank_title = 'Jack'
        elif self.rank == 12:
            self.rank_title = 'Queen'
        elif self.rank == 13:
            self.rank_title = 'King'
        elif self.rank == 14:
            self.rank_title = 'Ace'
               
    def initialize_suit(self):
        '''initialize suit of card, suit_title as string'''
        if self.suit == 1:
            self.suit_title = 'Spade'
        elif self.suit == 2:
            self.suit_title = 'Heart'
        elif self.suit == 3:
            self.suit_title = 'Diamond'
        elif self.suit == 4:
            self.suit_title = 'Club'
         
    def initialize(self):
        '''initialize attributes of Card'''
        self.initialize_rank()
        self.initialize_suit()
        
        self.title = self.rank_title + " of " + self.suit_title + "s"
        
def rank_to_string(rank):
    if rank == 2:
        return 'Two'
    elif rank == 3:
        return 'Three'
    elif rank == 4:
        return 'Four'
    elif rank == 5:
        return 'Five'
    elif rank == 6:
        return 'Six'
    elif rank == 7:
        return 'Seven'
    elif rank == 8:
        return 'Eight'
    elif rank == 9:
        return 'Nine'
    elif rank == 10:
        return 'Ten'
    elif rank == 11:
        return 'Jack'
    elif rank == 12:
        return 'Queen'
    elif rank == 13:
        return 'King'
    elif rank == 14:
        return 'Ace'       
         
            