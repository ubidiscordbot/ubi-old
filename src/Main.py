#Public Modules
import json
import os
import discord
import src.lib.essentials.commandHandler as commandHandler
import src.lib.essentials.socketHandler as socketHandler
import src.lib.essentials.create as create
import src.lib.runtimes.games.scrabble as Scrabble
import src.lib.essentials.connectionHandler as connection
import src.lib.runtimes.essentials.music as Music

create.create()

rts = socketHandler.Objs()

client = discord.Client()

con = connection.Connection(client, rts)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(";"):
        d_ = commandHandler.handle(message)
        if d_[0] == "Single":
            if d_[1][0][0] != "textPoll":
                for i in d_[1]:
                    if i[0] == "text":
                        await client.send_message(message.channel, i[1])
                    elif i[0] == "fileKeep":
                        await client.send_file(message.channel, i[1])
                    elif i[0] == "fileRemove":
                        await client.send_file(message.channel, i[1])
                        os.remove(i[1])
            else:
                await client.delete_message(message)
                m_ = await client.send_message(message.channel, d_[1][0][1])
                await client.add_reaction(m_, '👍')
                await client.add_reaction(m_, '👎')
        elif d_[0] == "Socket":
            f = open("server/servers/" + str(message.server.id) + ".json", "r")
            f_ = json.loads(f.read())
            f.close()
            if not f_[0] and d_[1] != "Music":
                if d_[1] == "Scrabble":
                    f = open("server/servers/" + message.server.id + ".json", "w")
                    f.write(json.dumps([True]))
                    f.close()
                    rts.create_socket([message.server.id, Scrabble.Main(message=message, client=client, obj=rts,
                                                                        connect=con)])
                    client.loop.create_task(rts.rtobj_get()[len(rts.rtobj_get()) - 1][1].scrabble_runtime())

            elif d_[1] == "Music":
                connected = False
                for i in rts.rtobj_get():
                    if i[0] == message.server.id:
                        connected = True
                if not connected:
                    if message.author.voice.voice_channel is not None:
                        rts.create_socket([message.server.id, Music.Music(client, message)])
                        client.loop.create_task(rts.rtobj_get()[len(rts.rtobj_get()) - 1][1].music_runtime())
                    else:
                        await client.send_message(message.channel, "[**Music**]Please join a voice channel before using $music")
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

    if message.content.startswith("$music"):
        for i in rts.rtobj_get():
            if i[0] == message.server.id:
                i[1].receive(message)

@client.event
async def on_server_join(server):
    print("Joined " + str(server))
    f = open("server/plusplus/" + str(server.id) + ".json", "w")
    f.write(json.dumps([]))
    f.close()
    f  = open("server/servers/" + str(server.id) + ".json", "w")
    f.write(json.dumps([False]))
    f.close()
    await client.send_message(server.default_channel, "https://i.cubeupload.com/HIkXQ5.png")

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name=';help to start'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)

client.loop.create_task(con.main_runtime())
client.run('Mjk3NTg4ODg2MzMzNTU0Njkw.C9CWOg.IT_jZBg6KxHgoSnQYCFRWiTEhng')
# Always change token to removed when committing
