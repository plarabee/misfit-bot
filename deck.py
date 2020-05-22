import random

from card import Card

class Deck:

    def __init__(self):
        self.cards = []
        self.build()
    
    def build(self):
        for suit in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
            value = 1
            for rank in ['Ace', 'Two', 'Three', 'Four',
                         'Five', 'Six', 'Seven', 'Eight',
                         'Nine', 'Ten', 'Jack', 'Queen', 'King']:
                self.cards.append(Card(suit, rank, value))
                value += 1
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self):
        drawn_card = self.cards[0]
        del self.cards[0]
        return drawn_card


