import src.lib.modules.memes
import src.lib.modules.comics
import src.lib.modules.plusplus
import src.lib.modules.flipcoin
import src.lib.modules.calc
import src.lib.modules.poll
import src.lib.modules.magicball
import src.lib.modules.define
import src.lib.modules.help
import src.lib.modules.clear
import src.lib.runtimes.games.mathwars
import src.lib.runtimes.games.reaction
import src.lib.runtimes.games.scrabble
import importlib


def handle(payload, mds, iph):
    raw = mds.get()[str(payload.server.id)]
    i2 = 0
    i4 = 0
    io = None
    external_command = False
    for i in raw:
        for i3 in raw[i]:
            if i3[0] == payload.content:
                external_command = True
                if not iph.has(i):
                    iph.add(importlib.import_module("src.lib.modules.ext." + i), i)
                io = iph.get()[0][iph.get()[1].index(i)]
                break
        i4 += 1
    if not external_command:
        if payload.content.lower() == ";help":
            return ["Single", src.lib.modules.help.main(payload, mds)]
        elif payload.content.lower() == ";flipcoin":
            return ["Single", src.lib.modules.flipcoin.main()]
        elif payload.content.lower() == ";comic":
            return ["Single", src.lib.modules.comics.main()]
        elif payload.content.lower().startswith(";poll"):
            return ["Single", src.lib.modules.poll.main(payload)]
        elif payload.content.lower().startswith(";define"):
            return ["Single", src.lib.modules.define.main(payload)]
        elif payload.content.lower().startswith(";weather"):
            return ["Single", src.lib.modules.weather.main(payload)]
        elif payload.content.lower() == ";meme":
            return ["Single", src.lib.modules.memes.main()]
        elif payload.content.lower() == ";stats":
            return ["Single", src.lib.modules.plusplus.main_stats(payload)]
        elif payload.content.lower().startswith(";++") or payload.content.lower().startswith(";--"):
            return ["Single", src.lib.modules.plusplus.main_alter(payload)]
        elif payload.content.lower().startswith(";calc "):
            return ["Single", src.lib.modules.calc.main(payload)]
        elif payload.content.lower().startswith(";scrabble"):
            return ["Socket", "Scrabble"]
        elif payload.content.lower().startswith(";music"):
            return ["Socket", "Music"]
        elif payload.content.lower().startswith(";8ball"):
            return ["Single", src.lib.modules.magicball.main()]
        elif payload.content.lower().startswith(";clear"):
            return ["Single", src.lib.modules.clear.main(payload)]
    else:
        return ["Single", io.main(payload)]
