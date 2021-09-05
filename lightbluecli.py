import lightblue
import subprocess
from time import sleep
import random

# This program is designed to tell a human playing against other humans what moves to make. In essence, the human acts as the bot's eyes and hands.

# Helper function to get a valid type and suit  
def getTypeAndSuit():
    while True:
        try:
            t = lightblue.CardTypes(input("Type: "))
            s = lightblue.CardSuits(input("Suit: "))
        except ValueError:
            print("Invalid choice.")
        else:
            return t, s

# Setup
bot = lightblue.LightBlue()
print("Card terminology:")
for cardType in lightblue.CardTypes:
    print(cardType.name + ":", cardType.value)
print("Suit terminology:")
for cardSuit in lightblue.CardSuits:
    print(cardSuit.name + ":", cardSuit.value)
print()
input("Ready to start, press enter to begin")
h = []
print("Please enter cards in hand (input blank text for type to finish)")
# Gets the bot's hand
while True:
    t = input("Type: ")
    if t == "":
        break
    t = lightblue.CardTypes(t)
    s = lightblue.CardSuits(input("Suit: "))
    h.append(lightblue.Card(t, s))
bot.startGame(h)

print()
print("When it is the bot's turn, press Enter (or type \"lose\" if it has lost), then enter the type and suit of the card on the top of the deck.")
while True:
    l = input("Ready: ")
    if l == "lose":
        print("Bot has lost.")
        break
    elif l != "":
        continue
    # Gets the top card
    t, s = getTypeAndSuit()
    # The magic happens here
    r = bot.play(lightblue.Card(t, s))
    res, card = r[0], r[1]
    if res == lightblue.PlayResults.SUCCESS:
        # The bot was able to play a card.
        print("Bot puts card", str(card), "on the deck.")
    elif res == lightblue.PlayResults.DRAWCARD:
        # The bot drew. You obviously have to tell it what it just drew.
        print("Bot draws a card.")
        print("Input the card's info")
        t, s = getTypeAndSuit()
        bot.hand.append(lightblue.Card(t, s))
    elif res == lightblue.PlayResults.CRAZYEIGHT:
        # The bot has played an eight.
        print("Bot plays an eight of", card[0].name,  "and sets the suit to", card[1].name)
    elif res == lightblue.PlayResults.WIN:
        # The bot won.
        print("Bot has won!")
        break
print("Bot says: Good game, and thanks for playing.")

