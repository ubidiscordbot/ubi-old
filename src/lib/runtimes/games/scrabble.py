import asyncio
import time
import math
import random
import re


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
    async def scrabble_runtime(self):
        await self.client.wait_until_ready()
        await self.client.send_message(self.message.channel, "```Welcome to Scrabble!```")
        await self.client.send_message(self.message.channel, "```Please choose a game mode```")
        await self.client.send_message(self.message.channel, "```1. One server game (^1) \n\n2. Two server game (^"
                                                             "2)```")
        second = get_second()
        while second + 30 > get_second():
            await asyncio.sleep(.01)
            if len(self.received) == 1:
                if self.received[0].content == "^1" or self.received[0].content == "^2":
                    break
        if second + 30 < get_second():
            await self.client.send_message(self.message.channel, "```Nobody started game, closing session```")
            self.obj.close_socket(self.message.server.id)
        elif self.received[0].content == "^2":
            self.received.pop(0)
            await self.client.send_message(self.message.channel, "```At least 2 players needed to start, do ^join to "
                                                                 "join your servers team, when everyone is ready do "
                                                                 "^start, if you wish to cancel the game do ^cancel```")
            while True:
                await asyncio.sleep(.01)
                if len(self.received) != 0:
                    if self.received[0].content == '^join':
                        self.team.append(self.received[0].author.name)
                        await self.client.send_message(self.message.channel, "```" +
                                                       self.received[0].author.name + " has joined the team!```")
                        self.received.pop(0)
                    elif self.received[0].content == '^cancel':
                        self.obj.close_socket(self.message.server.id)
                        break
                    elif self.received[0].content == "^start":
                        self.received.pop(0)
                        if len(self.team) >= 1:
                            await self.client.send_message(self.message.channel,
                                                       "```Searching for opposing server```")
                            self.connect.add_search(["Scrabble", self.message.server.id, self.message.server])
                            while True:
                                if len(self.connection) != 0:
                                    await self.client.send_message(self.message.channel, "```Server found! \n\nOpposing server: " +
                                                                   str(self.connection[1]) + "```")
                                    if self.conid == 0:
                                        self.direct.incoming_append(
                                            ["```Scrabble! Game starting in 20 seconds```", self.opid])
                                        await self.client.send_message(self.message.channel,
                                                                       "```Scrabble! Game starting in 20 seconds```")
                                        await asyncio.sleep(20)
                                        await self.client.send_message(self.message.channel, "```Scrabble!```")
                                        self.direct.incoming_append(["```Scrabble!```", self.opid])
                                        current_round = 1
                                        leaderboard = []
                                        self.received = []
                                        while current_round <= 2:
                                            q = form_question()
                                            await self.client.send_message(self.message.channel, "```Round " + str(
                                                current_round) + "\n\nLetters: "
                                                                           + q[1] + "```")
                                            self.direct.incoming_append(["```Round " + str(
                                                current_round) + "\n\nLetters: "
                                                                           + q[1] + "```", self.opid])
                                            round_start = get_second()
                                            while round_start + 30 > get_second():
                                                await asyncio.sleep(.01)
                                                if len(self.received) != 0 and self.received[0].author != self.client.user:
                                                    if len(self.connection_receive_list) != 0:
                                                        await self.client.send_message(self.message.channel,
                                                                                       "```" + self.connection_receive_list[0][
                                                                                           0].author.name + ": " +
                                                                                       self.connection_receive_list[0][
                                                                                           0].content + "```")

                                                    guess = convert_response(self.received[0].content)
                                                    obj = self.received[0]
                                                    self.received.pop(0)
                                                    if guess == q[2]:
                                                        await self.client.send_message(self.message.channel,
                                                                                       "```" + obj.author.name + " guessed " +
                                                                                       q[2] +
                                                                                       " and received " + str(
                                                                                           q[0]) + " points for their team!```")
                                                        self.direct.incoming_append(["```" + obj.author.name + " guessed " +
                                                                                       q[2] +
                                                                                       " and received " + str(
                                                                                           q[0]) + " points for their team!```", self.opid])
                                                        f = False
                                                        i2 = 0
                                                        name = str(self.message.server)
                                                        if obj.author.name not in self.team:
                                                            name = str(self.connection[1])
                                                        for i in leaderboard:
                                                            if i[0] == name:
                                                                leaderboard[i2][1] += q[0]
                                                                f = True
                                                                break
                                                            i2 += 1
                                                        if not f:
                                                            leaderboard.append([name, q[0]])
                                                        final_string = "Leaderboard" + "\n\n" + 'Name' + " " * 14 + "Points" + "\n\n"
                                                        n = form_new(leaderboard)
                                                        n.reverse()
                                                        leaderboard = n
                                                        num = 0
                                                        for i in n:
                                                            num += 1
                                                            multi = 18 - len(i[0])
                                                            final_string += str(num) + ". " + i[0] + " " * multi + str(
                                                                i[1]) + "\n"
                                                        await self.client.send_message(self.message.channel,
                                                                                       "```" + final_string + "```")

                                                        self.direct.incoming_append(["```" + final_string + "```", self.opid])
                                                        break
                                                    else:
                                                        await self.client.send_message(self.message.channel,
                                                                                       "```That's not it " +
                                                                                       obj.author.name + ". Keep Trying!```")
                                                        self.direct.incoming_append(["```That's not it " +
                                                                                       obj.author.name + ". Keep Trying!```", self.opid])
                                            if round_start + 30 <= get_second():
                                                await self.client.send_message(self.message.channel,
                                                                               "```Nobody guessed it, "
                                                                               "the answer was: " + q[2] + "```")
                                                self.direct.incoming_append(["```Nobody guessed it, "
                                                                               "the answer was: " + q[2] + "```", self.opid])
                                            current_round += 1
                                        n = form_new(leaderboard)
                                        n.reverse()
                                        if len(n) != 0:
                                            if len(n) > 1:
                                                if n[0][1] != n[1][1]:
                                                    await self.client.send_message(self.message.channel,
                                                                                   "```Game Finished! The winner is: " +
                                                                                   n[0][0] + "!```")
                                                    self.direct.incoming_append(["```Game Finished! The winner is: " +
                                                                               n[0][0] + "!```", self.opid])
                                                else:
                                                    await self.client.send_message(self.message.channel,
                                                                               "```Game Finished. Its a tie!```")
                                                    self.direct.incoming_append(["```Game Finished. Its a tie!```", self.opid])
                                            else:
                                                await self.client.send_message(self.message.channel,
                                                                               "```Game Finished! The winner is: " + n[0][0]
                                                                               + "!```")
                                                self.direct.incoming_append(["```Game Finished! The winner is: " + n[0][0]
                                                                               + "!```", self.opid])
                                        else:
                                            await self.client.send_message(self.message.channel,
                                                                           "```Game Finished. Nobody won```")
                                            self.direct.incoming_append(["```Game Finished. Nobody won```", self.opid])
                                        self.direct.incoming_append(["CLOSE", self.opid])
                                        self.obj.close_socket(self.message.server.id)
                                        return True
                                    else:
                                        while True:
                                            if len(self.connection_receive_list) != 0:
                                                if isinstance(self.connection_receive_list[0][0], str):
                                                    if not self.connection_receive_list[0][0] == "CLOSE":
                                                        await self.client.send_message(self.message.channel, self.connection_receive_list[0][0])
                                                    else:
                                                        self.obj.close_socket(self.message.server.id)
                                                        return True
                                                else:
                                                    await self.client.send_message(self.message.channel,
                                                                               "```" + self.connection_receive_list[0][0].author.name + ": " +
                                                                               self.connection_receive_list[0][0].content + "```")
                                                self.connection_receive_list.pop(0)
                                            await asyncio.sleep(.01)
                                        return True

                                await asyncio.sleep(.01)
                        else:
                            await self.client.send_message(self.message.channel,
                                                            "```Atleast " + str(2 - len(self.team)) + " people needed to "
                                                                                                        "start```")
                        self.received.pop(0)
        elif self.received[0].content == '^1':
            await self.client.send_message(self.message.channel, "```Scrabble! \n\nTutorial: The game of scrabble is "
                                                                 "composed of a game with 15 rounds, each round I "
                                                                 "will upload a scrambled word, your job is to "
                                                                 "decipher the word and comment your guess by using "
                                                                 "the ^ prefix (^ + guess). If your response is "
                                                                 "correct you will be awarded a certain amount of "
                                                                 "points based on the complexity of the problem "
                                                                 "the person with the most points at the end of "
                                                                 "the game wins \n\nStarting in 20 seconds...```")
            await asyncio.sleep(20)
            await self.client.send_message(self.message.channel, "```Scrabble!```")
            current_round = 1
            leaderboard = []
            self.received = []
            while current_round <= 15:
                q = form_question()
                await self.client.send_message(self.message.channel, "```Round " + str(current_round) + "\n\nLetters: "
                                               + q[1] + "```")
                round_start = get_second()
                while round_start + 30 > get_second():
                    await asyncio.sleep(.01)
                    if len(self.received) != 0 and self.received[0].author != self.client.user:
                        guess = convert_response(self.received[0].content)
                        obj = self.received[0]
                        self.received.pop(0)
                        if guess == q[2]:
                            await self.client.send_message(self.message.channel,
                                                           "```" + obj.author.name + " guessed " + q[2] +
                                                           " and received " + str(q[0]) + " points!```")
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
                            final_string = "Leaderboard" + "\n\n" + 'Name' + " " * 14 + "Points" + "\n\n"
                            n = form_new(leaderboard)
                            n.reverse()
                            leaderboard = n
                            num = 0
                            for i in n:
                                num += 1
                                multi = 18 - len(i[0])
                                final_string += str(num) + ". " + i[0] + " " * multi + str(i[1]) + "\n"
                            await self.client.send_message(self.message.channel, "```" + final_string + "```")
                            break
                        else:
                            await self.client.send_message(self.message.channel, "```That's not it " +
                                                           obj.author.name + ". Keep Trying!```")
                if round_start + 30 <= get_second():
                    await self.client.send_message(self.message.channel, "```Nobody guessed it, "
                                                                         "the answer was: " + q[2] + "```")
                current_round += 1
            n = form_new(leaderboard)
            n.reverse()
            if len(n) != 0:
                if len(n) > 1:
                    if n[0][1] != n[1][1]:
                        await self.client.send_message(self.message.channel, "```Game Finished! The winner is: " +
                                                       n[0][0] + "!```")
                    else:
                        await self.client.send_message(self.message.channel, "```Game Finished. Its a tie!```")
                else:
                    await self.client.send_message(self.message.channel, "```Game Finished! The winner is: " + n[0][0]
                                                   + "!```")
            else:
                await self.client.send_message(self.message.channel, "```Game Finished. Nobody won```")

            self.obj.close_socket(self.message.server.id)

    def receive(self, payload):
        self.received.append(payload)
        if len(self.connection) != 0:
            self.direct.incoming_append([payload, self.opid])
            if self.conid == 1:
                self.received.pop(0)

    def new_connection(self, conpath, payload, conid):
        self.connection = [conpath, payload, conid]
        self.conid = conid
        self.direct = conpath
        if self.conid == 1:
            self.opid = 0
        else:
            self.opid = 1

    def connection_receive(self, payload):
        self.connection_receive_list.append(payload)
        if self.conid == 0:
            self.received.append(payload[0])
