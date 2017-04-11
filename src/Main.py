#Public Modules
import json
import os
import discord
import src.lib.essentials.commandHandler as commandHandler
import src.lib.essentials.socketHandler as socketHandler
import src.lib.essentials.create as create
import src.lib.runtimes.games.scrabble as Scrabble
import src.lib.essentials.connectionHandler as connection

create.create()

rts = socketHandler.Objs()

client = discord.Client()

con = connection.Connection(client, rts)


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
            f = open("server/servers/" + str(message.server.id) + ".json", "r")
            f_ = json.loads(f.read())
            f.close()
            if not f_[0]:
                if d_[1] == "Scrabble":
                    f = open("server/servers/" + message.server.id + ".json", "w")
                    f.write(json.dumps([True]))
                    f.close()
                    rts.create_socket([message.server.id, Scrabble.Main(message=message, client=client, obj=rts,
                                                                        connect=con)])
                    client.loop.create_task(rts.rtobj_get()[len(rts.rtobj_get()) - 1][1].scrabble_runtime())
            else:
                await client.send_message(message.channel, "```There's already have a game running on the server, end or close it to "
                                          "start a"" new one```")
    if message.content.startswith("^"):
        f = open("server/servers/" + str(message.server.id) + ".json", "r")
        f_ = json.loads(f.read())
        f.close()
        if f_[0]:
            for i in rts.rtobj_get():
                if i[0] == message.server.id:
                    i[1].receive(payload=message)
                    break
@client.event
async def on_server_join(server):
    f = open("server/plusplus/" + str(server.id) + ".json", "w")
    f.write(json.dumps([]))
    f.close()
    f  = open("server/servers/" + str(server.id) + ".json", "w")
    f.write(json.dumps([False]))
    f.close()
    f = open("server/runtimes/" + str(server.id) + ".json", "w")
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

client.loop.create_task(con.main_runtime())
client.run('removed')
# Always change token to removed when committing
