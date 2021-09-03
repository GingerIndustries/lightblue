import lightblue
import subprocess
from time import sleep
import random
import threading
import screen2c

d = screen2c.Display()
d.write(" O" + " "*16 + "O ", 1)
d.write("  " + "_"*16, 2)
screenLock = threading.Lock()

def look():
    while True:
        sleep(random.randint(10, 35))
        screenLock.acquire()
        d.write("O" + " "*16 + "O  ")
        sleep(1)
        d.write("  O" + " "*16 + "O")
        sleep(1)
        d.write(" O" + " "*16 + "O ")
        screenLock.release()

def blink():
    while True:
        sleep(random.randint(5, 10))
        screenLock.acquire()
        d.write(" -" + " "*16 + "- ")
        screenLock.release()
        sleep(0.1)
        screenLock.acquire()
        d.write(" O" + " "*16 + "O ")
        screenLock.release()
        
threading.Thread(target = blink, daemon = True).start()
threading.Thread(target = look, daemon = True).start()

def _say(text, quiet = False):
    if quiet:
        s = subprocess.Popen(["espeak", "-v", "female3", "-a", "25", "\"" + str(text) + "\""])
    else:
        s = subprocess.Popen(["espeak", "-v", "female3", "\"" + str(text) + "\""])
    screenLock.acquire()
    d.write("  |" + "_"*14 + "|", 3)
    screenLock.release()
    s.wait()
    screenLock.acquire()
    d.write(" "*20, 3)
    screenLock.release()

def say(text, quiet = False):
    t = threading.Thread(target=_say, args=(text, quiet), daemon = True)
    t.start()
    
def getTypeAndSuit():
    while True:
        try:
            t = lightblue.CardTypes(input("Type: "))
            s = lightblue.CardSuits(input("Suit: "))
        except ValueError:
            print("Invalid choice.")
        else:
            return t, s

bot = lightblue.LightBlue()
print("Card terminology:")
for cardType in lightblue.CardTypes:
    print(cardType.name + ":", cardType.value)
print("Suit terminology:")
for cardSuit in lightblue.CardSuits:
    print(cardSuit.name + ":", cardSuit.value)
print()
say("I am ready to start.")
input("Ready to start, press enter to begin")
say("I shall give your human brains some time to prepare while I learn my deck.")
h = []
print("Please enter cards in hand (input blank text for type to finish)")
while True:
    t = input("Type: ")
    if t == "":
        break
    t = lightblue.CardTypes(t)
    s = lightblue.CardSuits(input("Suit: "))
    h.append(lightblue.Card(t, s))
bot.startGame(h)
say("It is time to begin. Good luck.")
print()
print("When it is the bot's turn, press Enter (or type \"lose\" if it has lost), then enter the type and suit of the card on the top of the deck.")
while True:
    l = input("Ready: ")
    if l == "lose":
        say("It seems I have lost. Ah well, maybe next time.")
        print("Bot has lost.")
        break
    elif l != "":
        say(l)
        continue
    t, s = getTypeAndSuit()
    r = bot.play(lightblue.Card(t, s))
    res, card = r[0], r[1]
    if res == lightblue.PlayResults.SUCCESS:
        say("I play my " + card.type.name + " of " + card.suit.name)
        print("Bot puts card", str(card), "on the deck.")
    elif res == lightblue.PlayResults.DRAWCARD:
        say("I draw a card.")
        print("Bot draws a card.")
        print("Input the card's info")
        t, s = getTypeAndSuit()
        bot.hand.append(lightblue.Card(t, s))
    elif res == lightblue.PlayResults.CRAZYEIGHT:
        say("I play an eight of " + card[0].name + ", and set the suit to" + card[1].name)
        print("Bot plays an eight of", card[0].name,  "and sets the suit to", card[1].name)
    elif res == lightblue.PlayResults.WIN:
        say("I have won!")
        sleep(1)
        say("of course", quiet = True)
        sleep(1.5)
        say("Regardless, good game! Thank you for playing")
        print("Bot has won!")
        break
print("Bot says: Good game, and thanks for playing.")

