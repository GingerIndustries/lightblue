import screen2c
import threading
import subprocess
from time import sleep
import random

d = screen2c.Display()
d.write("O" + " "*18 + "O", 1)
d.write("_"*20, 2)

running = True
def blink():
    while running:
        sleep(random.randint(5, 10))
        d.write("-" + " "*18 + "-")
        sleep(0.1)
        d.write("O" + " "*18 + "O")

b = threading.Thread(target = blink, daemon = True)
b.start()

def say(text, quiet = False):
    if quiet:
        s = subprocess.Popen(["espeak", "-v", "female3", "-a", "25", "\"" + str(text) + "\""])
    else:
        s = subprocess.Popen(["espeak", "-v", "female3", "\"" + str(text) + "\""])
    d.write("|" + "_"*18 + "|", 3)
    s.wait()
    d.write(" "*20, 3)

try:
    while True:
        i = input("> ")
        say(i)
except:
    del d
    running = False
    sleep(0.5)
    raise
