import discord
client = discord.Client()
lastVoteObjects = []


def main(message):
    vote = message.content.split(' ', 1)[1]
    return [["text", vote]]
