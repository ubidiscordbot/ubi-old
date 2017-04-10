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
    def __init__(self, client, message, obj):
        self.client = client
        self.message = message
        self.received = []
        self.obj = obj
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
            await self.client.send_message(self.message.channel, "```Game mode 2 is not supported for Scrabble yet, t"
                                                                 "his will be added in the future (Closing Session)```")
            self.obj.close_socket(self.message.server.id)
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
            while True:
                q = form_question()
                await self.client.send_message(self.message.channel, "```Round " + str(current_round) + "\n\nLetters: "
                                               + q[1])
                round_start = get_second()
                while round_start + 30 > get_second():
                    if len(self.received) != 0:
                        guess = convert_response(self.received[0].content)
                        obj = self.received[0]
                        self.received.pop(0)
                        if guess == q[2]:
                            await self.client.send_message(self.message.channel,
                                                           "```" + obj.author.name + " guessed " + q[2] +
                                                           " and received " + q[0] + " points!")
                            f = False
                            for i in leaderboard:
                                if i[0] == obj.author.name:
                                    i[1] += q[0]
                                    f = True
                            if not f:
                                leaderboard.append([obj.author.name, q[0]])
                            final_string = "Leaderboard" + "\n\n" + 'Name' + " " * 14 + "Credits" + "\n\n"
                            n = form_new(leaderboard)
                            n.reverse()
                            num = 0
                            for i in n:
                                num += 1
                                multi = 18 - len(i[0])
                                final_string += str(num) + ". " + i[0] + " " * multi + str(i[1]) + "\n"
                            await self.client.send_message(self.message.channel, "```" + final_string + "```")
                            break
                        else:
                            await self.client.send_message(self.message.channel, "``` That's not it " +
                                                           self.received[0].author.name + ". Keep Trying!")
                    await asyncio.sleep(0.01)
                if round_start + 30 > get_second():
                    await self.client.send_message(self.message.channel, "```Nobody guessed it, "
                                                                         "the answer was: " + q[1] + "```")
            n = form_new(leaderboard)
            n.reverse()
            await self.client.send_message(self.message.channel, "```Game Finished! The winner is: " + n[0][0] + "!")
            self.obj.close_socket(self.message.server.id)

    def receive(self, payload):
        self.received.append(payload)
