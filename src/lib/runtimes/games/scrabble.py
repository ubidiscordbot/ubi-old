import asyncio
import time
import math
import random
import re
import discord


def convert_response(string):
    l_ = list(string)
    l_.pop(0)
    return ''.join(l_)


def form_new(list_):
    old_list = list_
    new_values = []
    for i in list_:
        new_values.append([i[1]])
    sorted_values = sorted(new_values)
    i2 = 0
    while len(old_list) != 0:
        i = 0
        i2 += 1
        while i <= len(sorted_values) - 1:
            if old_list[0][1] == sorted_values[i][0]:
                sorted_values[i].insert(0, old_list[0][0])
                old_list.pop(0)
                break
            i += 1
    return sorted_values


def get_second():
    time_since_1970 = time.time()
    time_since_2000 = math.floor(time_since_1970 + 60 * 60 * 24 * 365 * 30)
    return time_since_2000


def form_question():
    f = open("server/assets/words.txt", "r")
    word_ = f.readlines()[random.randint(1, 1000)]
    word = re.findall(r"\S+", word_)[0]
    difficulty = len(word)
    f.close()
    xl = []
    for i in word:
        xl.append(i)
    final_q = []
    while len(xl) != 0:
        item = random.randint(0, len(xl) - 1)
        final_q.append(xl[item])
        xl.pop(item)
    return [difficulty, ''.join(final_q), word]


class Main:
    def __init__(self, client, message, obj, connect):
        self.client = client
        self.message = message
        self.received = []
        self.obj = obj
        self.connection = []
        self.connection_receive_list = []
        self.conid = "NAN"
        self.team = []
        self.connect = connect
        self.opid = "NAN"
        self.other_team = []
    async def scrabble_runtime(self):
        await self.client.wait_until_ready()
        await self.client.send_message(self.message.channel,
                                       embed=discord.Embed(title="Welcome to Scrabble!",
                                                           description="Please choose a game mode: \n\n 1. One server"
                                                                       " game (^1) \n\n2. Two server game (^2)", color=
                                                           0xe67e22))
        second = get_second()
        while second + 30 >= get_second():
            await asyncio.sleep(.01)
            if len(self.received) == 1:
                if self.received[0].content == "^1" or self.received[0].content == "^2":
                    break
                else:
                    self.received.pop(0)
        if second + 30 <= get_second():
            await self.client.send_message(self.message.channel
                                           , embed=discord.Embed(title="Game Alert"
                                                                 , description="Nobody started game, closing session."
                                                                 , color=0x9b59b6))
            self.obj.close_socket(self.message.server.id)
        elif self.received[0].content == "^2":
            self.received.pop(0)
            await self.client.send_message(self.message.channel
                                           , embed=discord.Embed(title="Lobby"
                                                                 , description="At least 2 players needed to start, do"
                                                                               " **^join** to "
                                                                 "join your server's team. Once everyone is ready do "
                                                                 "**^start**. If you wish to cancel the game do "
                                                                               "**^cancel**"
                                                                 , color=0xe67e22))
            while True:
                await asyncio.sleep(.01)
                if len(self.received) != 0:
                    if self.received[0].content == '^join':
                        if not self.received[0] in self.team:
                            self.team.append(str(self.received[0].author))
                            await self.client.send_message(self.message.channel
                                                           , embed=discord.Embed(title="Lobby"
                                                                                 ,
                                                                                 description="**" +
                                                           self.received[0].author.name + "** has joined the team!"
                                                                                 , color=0xe67e22))
                        else:
                            await self.client.send_message(self.message.channel
                                                           , embed=discord.Embed(title="Lobby"
                                                                                 ,
                                                                                 description="**" +
                                                                                             self.received[
                                                                                                 0].author.name + "** you already joined the team!"
                                                                                 , color=0xe67e22))
                        self.received.pop(0)
                    elif self.received[0].content == '^cancel':
                        await self.client.send_message(self.message.channel, embed=discord.Embed(title="Game Alert"
                                                                                                 , description=
                                                                                                 "Game was forcibly"
                                                                                                 " closed by client",
                                                                                                 color=0x9b59b6))
                        self.received.pop(0)
                        self.obj.close_socket(self.message.server.id)
                        return None
                    elif self.received[0].content == "^start":
                        self.received.pop(0)
                        if len(self.team) >= 1:
                            await self.client.send_message(self.message.channel, embed=discord.Embed(title="Lobby",
                                                                                                     description=
                                                                                                     "Searching"
                                                                                                     " for an"
                                                                                                     " opposing server",
                                                                                                     color=0xe67e22)
                                                           )
                            self.connect.add_search(["Scrabble", self.message.server.id, self.message.server, self.team])
                            while True:
                                if len(self.received) != 0:
                                    if self.received[0].content == '^cancel':
                                        await self.client.send_message(self.message.channel,
                                                                       embed=discord.Embed(title="Game Alert"
                                                                                           , description=
                                                                                           "Game was forcibly"
                                                                                           " closed by client",
                                                                                           color=0x9b59b6))
                                        self.received.pop(0)
                                        self.obj.close_socket(self.message.server.id)
                                        return None
                                if len(self.connection) != 0:
                                    await self.client.send_message(self.message.channel
                                                                   , embed=discord.Embed(title="Lobby"
                                                                                         , description="Server found!"
                                                                                                       "\nOpposing"
                                                                                                       " server: *" +
                                                                                                       str(self.connection[1]) + "*"
                                                                                         , color=0xe67e22))
                                    if self.conid == 0:
                                        embed_obj = discord.Embed(title="Scrabble"
                                                                  , description="Game starting in 20 seconds"
                                                                  , color=0xe67e22)
                                        self.direct.incoming_append(
                                            [embed_obj, self.opid, "Bot"])
                                        await self.client.send_message(self.message.channel, embed=embed_obj)
                                        await asyncio.sleep(20)
                                        current_round = 1
                                        leaderboard = []
                                        self.received = []
                                        while current_round <= 15:
                                            q = form_question()
                                            embed_obj = discord.Embed(title="Round " + str(current_round)
                                                                      , description="\nLetters: " + q[1],
                                                                      color=0xe67e22)
                                            await self.client.send_message(self.message.channel, embed=embed_obj)
                                            self.direct.incoming_append([embed_obj, self.opid, "Bot"])
                                            round_start = get_second()
                                            while round_start + 30 > get_second():
                                                await asyncio.sleep(.01)
                                                if len(self.received) != 0 and self.received[0].author \
                                                        != self.client.user:
                                                    if str(self.received[0].author) in self.team or \
                                                                    str(self.received[0].author) in self.other_team:

                                                        if len(self.connection_receive_list) != 0:
                                                            embed_obj = discord.Embed(description="**" + self.connection_receive_list[0][0].author.name
                                                                                                  + "@" + str(self.connection[1]) + "**: " + self.connection_receive_list[0][0].content
                                                                                      , color=0xe84d00)
                                                            await self.client.send_message(self.message.channel, embed=embed_obj)
                                                            self.connection_receive_list.pop(0)

                                                        guess = convert_response(self.received[0].content)
                                                        obj = self.received[0]
                                                        self.received.pop(0)
                                                        if guess == q[2]:
                                                            await self.client.send_message(self.message.channel,
                                                                                           "**" + obj.author.name + "** guessed **" +
                                                                                           q[2] +
                                                                                           "** and received **" + str(
                                                                                               q[0]) + "** points for their team!")
                                                            self.direct.incoming_append(["**" + obj.author.name + "** guessed **" +
                                                                                           q[2] +
                                                                                           "** and received **" + str(
                                                                                               q[0]) + "** points for their team!", self.opid, "Bot"])
                                                            f = False
                                                            i2 = 0
                                                            name = str(self.message.server)
                                                            if str(obj.author) not in self.team:
                                                                name = str(self.connection[1])
                                                            for i in leaderboard:
                                                                if i[0] == name:
                                                                    leaderboard[i2][1] += q[0]
                                                                    f = True
                                                                    break
                                                                i2 += 1
                                                            if not f:
                                                                leaderboard.append([name, q[0]])
                                                            final_string = ""
                                                            n = form_new(leaderboard)
                                                            n.reverse()
                                                            leaderboard = n
                                                            num = 0
                                                            for i in n:
                                                                num += 1
                                                                multi = 18 - len(i[0])
                                                                final_string += str(num) + ". " + i[0] + " " * multi + str(
                                                                    i[1]) + "\n"
                                                            embed_obj = discord.Embed(title="Leaderboard", description=
                                                                                      final_string, color=0xe67e22)
                                                            await self.client.send_message(self.message.channel,
                                                                                           embed=embed_obj)

                                                            self.direct.incoming_append([embed_obj, self.opid, "Bot"])
                                                            break
                                                        else:
                                                            await self.client.send_message(self.message.channel,
                                                                                           "That's not it, **" +
                                                                                           obj.author.name + "**. Keep Trying!")
                                                            self.direct.incoming_append(["That's not it, **" +
                                                                                           obj.author.name + "**. Keep Trying!", self.opid, "Bot"])
                                                    else:
                                                        obj = self.received[0]
                                                        self.received.pop(0)
                                                        await self.client.send_message(self.message.channel,
                                                                                       "**" +
                                                                                       obj.author.name + "** is not in a team, and therefore cant participate until a new game is started.")
                                                        self.direct.incoming_append(["**" +
                                                                                       obj.author.name + "** is not in a team, and therefore cant participate until a new game is started.",
                                                                                     self.opid, "Bot"])

                                            if round_start + 30 <= get_second():
                                                await self.client.send_message(self.message.channel,
                                                                               "Nobody guessed correctly, "
                                                                               "the answer was: **" + q[2] + "**")
                                                self.direct.incoming_append(["Nobody guessed correctly, "
                                                                               "the answer was: **" + q[2] + "**", self.opid, "Bot"])
                                            current_round += 1
                                        n = form_new(leaderboard)
                                        n.reverse()
                                        if len(n) != 0:
                                            if len(n) > 1:
                                                if n[0][1] != n[1][1]:
                                                    embed_obj = discord.Embed(title="Scrabble"
                                                                              , description="Game Finished!"
                                                                                            " The winner is **" + n[0][0] + "**!"
                                                                              , color=0xe67e22)
                                                    await self.client.send_message(self.message.channel, embed=embed_obj)
                                                    self.direct.incoming_append([embed_obj, self.opid, "Bot"])
                                                else:
                                                    embed_obj = discord.Embed(title="Scrabble"
                                                                              , description="Game Finished!"
                                                                                            " **Its a tie**!"
                                                                              , color=0xe67e22)
                                                    await self.client.send_message(self.message.channel, embed=embed_obj)
                                                    self.direct.incoming_append([embed_obj, self.opid, "Bot"])
                                            else:
                                                embed_obj = discord.Embed(title="Scrabble"
                                                                          , description="Game Finished!"
                                                                                        " The winner is **" + n[0][
                                                                                            0] + "**!"
                                                                          , color=0xe67e22)
                                                await self.client.send_message(self.message.channel, embed=embed_obj)
                                                self.direct.incoming_append([embed_obj, self.opid, "Bot"])
                                        else:
                                            embed_obj = discord.Embed(title="Scrabble"
                                                                      , description="Game Finished!"
                                                                                    " **Nobody won**!"
                                                                      , color=0xe67e22)
                                            await self.client.send_message(self.message.channel, embed=embed_obj)
                                            self.direct.incoming_append([embed_obj, self.opid, "Bot"])
                                        self.direct.incoming_append(["CLOSE", self.opid, "Bot"])
                                        self.obj.close_socket(self.message.server.id)
                                        return True
                                    else:
                                        while True:
                                            if len(self.connection_receive_list) != 0:
                                                if self.connection_receive_list[0][2] == "User":
                                                    embed_obj = discord.Embed(description="**" + self.connection_receive_list[0][0].author.name
                                                                                          + "@" + str(self.connection[1]) + "**: " + self.connection_receive_list[0][0].content
                                                                              , color=0xe84d00)
                                                    await self.client.send_message(self.message.channel, embed=embed_obj)
                                                elif self.connection_receive_list[0][2] == "Bot":
                                                    if isinstance(self.connection_receive_list[0][0], discord.Embed):
                                                        await self.client.send_message(self.message.channel
                                                                                        , embed=self.connection_receive_list[0][0])
                                                    elif isinstance(self.connection_receive_list[0][0], str):
                                                        if self.connection_receive_list[0][0] == "CLOSE":
                                                            self.obj.close_socket(self.message.server.id)
                                                            return True
                                                        else:
                                                            await self.client.send_message(self.message.channel, self.connection_receive_list[0][0])
                                                self.connection_receive_list.pop(0)
                                            await asyncio.sleep(.01)
                                        return True

                                await asyncio.sleep(.01)
                        else:
                            if 2 - len(self.team) >= 2:
                                embed_obj = discord.Embed(title="Lobby"
                                                          , description="**" + str(2 - len(self.team)) + "** more people needed to begin!"
                                                          , color=0xe84d00)
                                await self.client.send_message(self.message.channel, embed=embed_obj)
                            else:
                                embed_obj = discord.Embed(title="Lobby"
                                                          , description="**" + str(
                                        2 - len(self.team)) + "** more person needed to begin!"
                                                          , color=0xe84d00)
                                await self.client.send_message(self.message.channel, embed=embed_obj)
                    else:
                        self.received.pop(0)
        elif self.received[0].content == '^1':
            embed_obj = discord.Embed(title="Scrabble", description="**Tutorial**: The game of scrabble "
                                                                 "is "
                                                                 "composed of a game with 15 rounds. each round I "
                                                                 "will upload a scrambled word; your job is to "
                                                                 "decipher the word and comment your guess by using "
                                                                 "the **^** prefix (^ + your guess). If your response is "
                                                                 "correct you will be awarded a certain amount of "
                                                                 "points based on the difficulty of the problem. "
                                                                 "the person with the most points at the end of "
                                                                 "the game wins \n\n**Beginning in 20 seconds...**"
                                      ,color=0xe67e22)
            await self.client.send_message(self.message.channel, embed=embed_obj)
            await asyncio.sleep(20)
            current_round = 1
            leaderboard = []
            self.received = []
            while current_round <= 15:
                q = form_question()
                embed_obj = discord.Embed(title="Round " + str(current_round)
                                          , description="\nLetters: " + q[1],
                                          color=0xe67e22)
                await self.client.send_message(self.message.channel, embed=embed_obj)
                round_start = get_second()
                while round_start + 30 > get_second():
                    await asyncio.sleep(.01)
                    if len(self.received) != 0 and self.received[0].author != self.client.user:
                        guess = convert_response(self.received[0].content)
                        obj = self.received[0]
                        self.received.pop(0)
                        if guess == q[2]:
                            await self.client.send_message(self.message.channel,
                                                           "**" + obj.author.name + "** guessed **" + q[2] +
                                                           "** and received **" + str(q[0]) + "** points!")
                            f = False
                            i2 = 0
                            for i in leaderboard:
                                if i[0] == obj.author.name:
                                    leaderboard[i2][1] += q[0]
                                    f = True
                                    break
                                i2 += 1
                            if not f:
                                leaderboard.append([obj.author.name, q[0]])
                            final_string = ""
                            n = form_new(leaderboard)
                            n.reverse()
                            leaderboard = n
                            num = 0
                            for i in n:
                                num += 1
                                multi = 18 - len(i[0])
                                final_string += str(num) + ". " + i[0] + " " * multi + "**" + str(i[1]) + "** \n"
                            embed_obj = discord.Embed(title="Leaderboard", description=final_string, color=0xe67e22)
                            await self.client.send_message(self.message.channel, embed=embed_obj)
                            break
                        else:
                            await self.client.send_message(self.message.channel, "That's not it, **" +
                                                           obj.author.name + "**. Keep Trying!")
                if round_start + 30 <= get_second():
                    await self.client.send_message(self.message.channel, "Nobody guessed it, "
                                                                         "the answer was: **" + q[2] + "**")
                current_round += 1
            n = form_new(leaderboard)
            n.reverse()
            if len(n) != 0:
                if len(n) > 1:
                    if n[0][1] != n[1][1]:
                        embed_obj = discord.Embed(title="Scrabble"
                                                  , description="Game Finished!"
                                                                " The winner is **" + n[0][0] + "**!"
                                                  , color=0xe67e22)
                        await self.client.send_message(self.message.channel, embed=embed_obj)
                    else:
                        embed_obj = discord.Embed(title="Scrabble"
                                                  , description="Game Finished!"
                                                                " **Its a tie**!"
                                                  , color=0xe67e22)
                        await self.client.send_message(self.message.channel, embed=embed_obj)
                else:
                    embed_obj = discord.Embed(title="Scrabble"
                                              , description="Game Finished!"
                                                            " The winner is **" + n[0][
                                                                0] + "**!"
                                              , color=0xe67e22)
                    await self.client.send_message(self.message.channel, embed=embed_obj)
            else:
                embed_obj = discord.Embed(title="Scrabble"
                                          , description="Game Finished!"
                                                        " **Nobody won**!"
                                          , color=0xe67e22)
                await self.client.send_message(self.message.channel, embed=embed_obj)

            self.obj.close_socket(self.message.server.id)

    def receive(self, payload):
        self.received.append(payload)
        if len(self.connection) != 0:
            self.direct.incoming_append([payload, self.opid, "User"])
            if self.conid == 1:
                self.received.pop(0)

    def new_connection(self, conpath, payload, conid, ot):
        self.connection = [conpath, payload, conid]
        self.conid = conid
        self.direct = conpath
        self.other_team = ot
        if self.conid == 1:
            self.opid = 0
        else:
            self.opid = 1

    def connection_receive(self, payload):
        self.connection_receive_list.append(payload)
        if self.conid == 0:
            self.received.append(payload[0])