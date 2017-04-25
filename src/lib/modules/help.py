import discord


def generate_string(id, mds):
    raw = mds.get()[str(id)]
    final_string = ""
    for i in raw:
        final_string += "\n\n__" + i + "__\n\n"
        for i3 in raw[i]:
            final_string += "**" + i3[0] + "** - " + i3[1] + "\n"
    return final_string


def main(message, mds):
    string = generate_string(message.server.id, mds)
    embed = discord.Embed(description="""**Ubi Help**

        __Standard commands__

            **;flipcoin** - flips a coin
            **;comic** - uploads a comic from xkcd
            **;meme** -  uploads a meme from memes.com
            **;scrabble** - starts a game of scrabble
            **;poll <text>** - starts a basic yes/no poll
            **;define <word>** - grabs the definition of any word
            **;8ball <question>** - inquires the all seeing magic 8ball
            **;calc <expression>** - evaluates any arithmetic expression
            **;clear <amount of messages>** - removes the amount of messages specified from a channel

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
            """ + string, color=0xe74c3c)
    return [["textEmbed", embed]]