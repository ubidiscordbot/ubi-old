import json
import time
import math
import asyncio


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


class Update:
    def __init__(self, client):
        self.last = get_second()
        self.client = client

    async def main(self):
        while True:
            if self.last + 1200 < get_second():
                await self.call()
                self.last = get_second()
            await asyncio.sleep(1)

    async def call(self):
        f = open("server/games/gamerank.json", "r")
        n_ = form_new(json.loads(f.read()))
        n_.reverse()
        f.close()
        f = open("server/games/gamerank.json", "w")
        f.write(json.dumps(n_))
        f.close()
        f = open("server/news/news.json", "r")
        f_ = json.loads(f.read())
        if len(f_) != 0:
            for i in f_:
                for server in self.client.servers:
                    await self.client.send_message(server.default_channel, i)
        f_.close()
        f = open("server/news/news.json", "w")
        f.write(json.dumps([]))
        f.close()
