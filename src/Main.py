#Public Modules
import discord
import random
import os
import json
import time
import math
import asyncio
import re
import urllib.request

#Local Modules
import src.lib.essentials.commandHandler as commandHandler
import src.create as create
create.create()

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$"):
        d_ = commandHandler.handle(message)
        if d_[0] == "Single":
            for i in d_[1]:
                if i[0] == "text":
                    await client.send_message(message.channel, i[1])
                elif i[0] == "fileKeep":
                    await client.send_file(message.channel, i[1])
                elif i[0] == "fileRemove":
                    await client.send_file(message.channel, i[1])
                    os.remove(i[1])
        elif d_[0] == "Socket":
            client.loop.create_task(d_[1]())

@client.event
async def on_server_join(server):
    f = open("server/plusplus/" + str(server.id) + ".json", "w")
    f.write(json.dumps([]))
    f.close()
    await client.send_message(server.default_channel, "http://i.cubeupload.com/Cn0KwZ.png")
    await client.send_message(server.default_channel, "http://i.cubeupload.com/ohkUoP.png")
    await client.send_message(server.default_channel, "http://i.cubeupload.com/acGvxZ.png")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('Mjk3NTg4ODg2MzMzNTU0Njkw.C8DAoA.cD5bR5QA_Fo6-t3WyzUOosBRI_A')