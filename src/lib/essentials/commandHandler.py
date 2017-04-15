import src.lib.modules.memes
import src.lib.modules.comics
import src.lib.modules.plusplus
import src.lib.modules.flipcoin
import src.lib.modules.calc
import src.lib.modules.poll
import src.lib.modules.magicball
import src.lib.modules.define
import src.lib.runtimes.games.mathwars
import src.lib.runtimes.games.reaction
import src.lib.runtimes.games.scrabble
import discord


def handle(payload):
    if payload.content.lower() == ";help":
        embed = discord.Embed(description="""**Ubi Help**

    __Standard commands__

        **;flipcoin** - flips a coin
        **;comic** - uploads a comic from xkcd
        **;meme** -  uploads a meme from memes.com
        **;scrabble** - starts a game of scrabble
        **;poll <text>** - starts a basic yes/no poll
        **;define <word>** - grabs the definition of any word
        **;8ball <question>** - inquires the all seeing magic 8ball
        **;weather <location>** - grabs weather data for specified location
        **;calc <expression>** - evaluates any arithmetic expression

    __Music commands__

        **;music** - initializes music and joins the channel you're in
        **;music add <url>** - replace (url) with youtube link, adds link to quene
        **;music skip** -  adds vote to skip current song (2 votes = skip)
        **;music playlist** - shows all songs in the playlist quene
        **;music move** - moves bot to the voice channel you're in
        **;music pause** - pauses the current song

    __Plus Plus commands__

        **;stats** - gets a leaderboard of plus plus scores
        **;++<user>** - adds a point to a specific user (don't put a space between the last + and the users name)
        **;--<user>** - removes a point from a specific user (don't put a space between the last - and the users name)
        """)
        return ["Single", [["textEmbed", embed]]]
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
