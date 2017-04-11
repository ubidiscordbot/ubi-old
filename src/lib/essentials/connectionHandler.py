import asyncio

class Connection:
    def __init__(self, client, rtobj):
        self.servers_searching_scrabble = []
        self.servers_searching_reaction = []
        self.servers_searching_mathwars = []
        self.client = client
        self.rtobj = rtobj

    def add_search(self, payload):
        if payload[0] == "Scrabble":
            self.servers_searching_scrabble.append([payload[1], payload[2], payload[3]])
        if payload[0] == "Reaction":
            self.servers_searching_reaction.append([payload[1], payload[2], payload[3]])
        if payload[0] == "Mathwars":
            self.servers_searching_mathwars.append([payload[1], payload[2], payload[3]])

    async def main_runtime(self):
        while True:
            if len(self.servers_searching_scrabble) >= 2:
                new = ConnectionRuntime(self.client, [self.servers_searching_scrabble[0], self.servers_searching_scrabble[1]],  self.rtobj)
                self.client.loop.create_task(new.connection_runtime())
                self.servers_searching_scrabble.pop(0)
                self.servers_searching_scrabble.pop(0)
            await asyncio.sleep(0.01)


class ConnectionRuntime():
    def __init__(self, client, servers, rtobj):
        self.client = client
        self.servers = servers
        self.rtobj = rtobj
        self.incoming = []
        self.closed = False

    async def connection_runtime(self):
        connection_data = []
        i2 = 0
        for i in self.rtobj.rtobj_get():
            if i[0] in self.servers[0] or i[0] in self.servers[1]:
                connection_data.append([i[0], i[1]])
                if len(connection_data) == 2:
                    break
            i2 += 1
        connection_data[0][1].new_connection(self, self.servers[1][1], 0, self.servers[1][2])
        connection_data[1][1].new_connection(self, self.servers[0][1], 1, self.servers[0][2])
        while True:
            if len(self.incoming) != 0:
                connection_data[self.incoming[0][1]][1].connection_receive(self.incoming[0])
                self.incoming.pop(0)
            if self.closed:
                break
            await asyncio.sleep(.01)

    def incoming_append(self, payload):
        self.incoming.append(payload)

    def close(self):
        self.closed = True

