import urllib.request
import os
import random


def main():
    developed = "http://images.memes.com/meme/13" + str(random.randint(10000, 79000))
    nameVar = str(random.randint(1000, 9999))
    urllib.request.urlretrieve(developed, "server/bin/memes/" + str(nameVar) + ".gif")
    return [["fileRemove", "server/bin/memes/" + str(nameVar) + ".gif"]]