import json


class MdHandle:
    def __init__(self, client):
        self.mds = {}
        for server in client.servers:
            try:
                f = open("server/servers/" + str(server.id) + ".json", "r")
                f_ = json.loads(f.read())
                self.mds[str(server.id)] = f_
            except FileNotFoundError:
                pass

    def get(self):
        return self.mds

    def update(self, server_id):
        f = open("server/servers/" + str(server_id) + "json", "r")
        f_ = json.loads(f.read())
        self.mds[str(server_id)] = f_
