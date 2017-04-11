#This file will throw a lot of errors, just dump files/code here for later use

async def MainLoop():
    await client.wait_until_ready()
    print("runningMainLoop")
    while not client.is_closed:
        time_since_1970 = time.time()
        time_since_2000 = math.floor(time_since_1970 + 60 * 60 * 24 * 365 * 30)
        for server in client.servers:
            f = open(os.path.join("serverFiles", server.id + ".json"), "r")
            dec = json.loads(f.read())
            f.close()
            f = open(os.path.join("serverFiles", server.id + ".json"), "w")
            if dec[0] + 60 < time_since_2000 and dec[1] == 'NAN':
                dec[0] = 'NAN'
                dec[1] = time_since_2000
                await client.send_message(server.default_channel,
                                            "Hey im sad, can someone cheer me up using #animate ubi")
                f.write(json.dumps(dec))
                f.close()
            elif dec[1] == "NAN":
                dec[0] = time_since_2000
                f.write(json.dumps(dec))
                f.close()
            elif dec[1] != 'NAN' and dec[1] + 60 < time_since_2000:
                await client.send_message(server.default_channel, "You guys never listen ):")
                await client.send_message(server.default_channel, "```Happiness -1```")
                dec[1] = 'NAN'
                f.write(json.dumps(dec))
                f.close()
            elif dec[1] != 'NAN':
                dec[1] = time_since_2000
                f.write(json.dumps(dec))
                f.close()
        await asyncio.sleep(1)


if message.content.lower() == "#animate ubi":
    f = open(os.path.join("serverFiles", str(message.server.id) + ".json"), "r")
    dec = json.loads(f.read())
    time_since_1970 = time.time()
    time_since_2000 = math.floor(time_since_1970 + 60 * 60 * 24 * 365 * 30)
    if dec[1] != 'NAN':
        if dec[1] + 60 > time_since_2000:
            await
            client.send_message(message.channel, "Thankyou @" + message.author + " I feel much better now")
            await
            client.send_message(message.channel, "```Happiness +1```")
            dec[0] = time_since_2000
            dec[1] = 'NAN'