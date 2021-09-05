from enum import Enum

# Used to represent cards
class Card():
    def __init__(self, type_, suit):
        self.suit = suit
        self.type = type_

    def __str__(self):
        return "Card (suit: " + self.suit.name + " type: " + self.type.name + ")"

# The types of cards
class CardTypes(Enum):
    ACE = "a"
    KING = "k"
    QUEEN = "q"
    JACK = "j"
    JOKER = "?"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"

# The suits of cards
class CardSuits(Enum):
    HEARTS = "h"
    SPADES = "s"
    CLUBS = "c"
    DIAMONDS = "d"

# Results of a move
class PlayResults(Enum):
    SUCCESS = 0
    DRAWCARD = 1
    CRAZYEIGHT = 2
    WIN = 3

class LightBlue():
    def __init__(self):
        self.hand = []
        self.topcard = None

    '''Should be called when teh game starts.
        Pass it a list of Card objects
    '''
    def startGame(self, hand):
        self.hand = hand

    '''The actual gameplay code.
        Pass it a Card object representing the card on top of the deck.
        Returns a tuple containing a PlayResult and related data.
    '''
    def play(self, topcard):
        for card in self.hand:
            if (card.suit == topcard.suit or card.type == topcard.type) and not card.type == CardTypes.EIGHT:
                self.hand.remove(card)
                if len(self.hand) == 0:
                    return (PlayResults.WIN, None)
                return (PlayResults.SUCCESS, card)
        for card in self.hand:
            if card.type == CardTypes.EIGHT:
                self.hand.remove(card)
                if len(self.hand) == 0:
                    return (PlayResults.WIN, None)
                cardCount = {"h": 0, "s": 0, "c": 0, "d": 0}
                for counter in self.hand:
                    cardCount[counter.suit.value] += 1
                #print(cardCount)
                return (PlayResults.CRAZYEIGHT, (card.suit, CardSuits({cardCount[x]:x for x in cardCount}[max(cardCount.values())])))
        return (PlayResults.DRAWCARD, None)
        
