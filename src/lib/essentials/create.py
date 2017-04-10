import os
import urllib.request


def create():
    if not os.path.exists("server/servers"):
        os.makedirs("server/servers")
    if not os.path.exists("server/plusplus"):
        os.makedirs("server/plusplus")
    if not os.path.exists("server/assets"):
        os.makedirs("server/assets")
        urllib.request.urlretrieve("https://u.cubeupload.com/Enclo/Heads.png", "server/assets/Heads.png")
        urllib.request.urlretrieve("https://u.cubeupload.com/Enclo/Tails.png", "server/assets/Tails.png")
        urllib.request.urlretrieve("https://raw.githubusercontent.com/encloinc/ubitextassets/master/words.txt",
                                   "server/assets/words.txt")
    if not os.path.exists("server/games/"):
        os.makedirs("server/games")
    if not os.path.exists("server/bin/comics"):
        os.makedirs("server/bin/comics")
    if not os.path.exists("server/bin/memes"):
        os.makedirs("server/bin/memes")
    if not os.path.exists("server/runtimes"):
        os.makedirs("server/runtimes")

create()
