import src.lib.modules.memes
import src.lib.modules.comics
import src.lib.modules.plusplus
import src.lib.modules.flipcoin
import src.lib.modules.calc
import src.lib.modules.poll
import src.lib.runtimes.games.mathwars
import src.lib.runtimes.games.reaction
import src.lib.runtimes.games.scrabble


def handle(payload):
    if payload.content.lower() == ";help":
        return ["Single", [["text", """**Ubi Help**

    __Standard commands__

        **;flipcoin** - flips a coin
        **;comic** - uploads a comic from xkcd
        **;meme** -  uploads a meme from memes.com
        **;scrabble** - starts a game of scrabble

    __Music commands__

        **;music add <url>** - replace (url) with youtube link, adds link to quene
        **;music skip** -  adds vote to skip current song (2 votes = skip)
        **;music playlist** - shows all songs in the playlist quene
        **;music move** - moves bot to the voice channel you're in

    __Plus Plus commands__

        **;stats** - gets a leaderboard of plus plus scores
        **;++<user>** - adds a point to a specific user (don't put a space between the last + and the users name)
        **;--<user>** - removes a point from a specific user (don't put a space between the last - and the users name)
        """]]]
    elif payload.content.lower() == ";flipcoin":
        return ["Single", src.lib.modules.flipcoin.main()]
    elif payload.content.lower() == ";comic":
        return ["Single", src.lib.modules.comics.main()]
    elif payload.content.lower() == ";vote":
        return ["Single", src.lib.modules.poll.main()]
    elif payload.content.lower() == ";meme":
        return ["Single", src.lib.modules.memes.main()]
    elif payload.content.lower() == ";meme":
        return ["Single", src.lib.modules.poll.main()]
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
    elif payload.content.lower().startswith(";poll"):
        return ["Single", src.lib.modules.poll.main(payload)]
