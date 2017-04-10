import json


class Objs:
    def __init__(self):
        self.rt_obj = []

    def close_socket(self, id_):
        i2 = 0
        for i in self.rt_obj:
            if i[0] == id_:
                self.rt_obj.pop(i2)
                break
            i2 += 1
        f = open("server/servers/" + id_ + ".json", "w")
        f.write(json.dumps([False]))
        f.close()

    def create_socket(self, sk):
        self.rt_obj.append(sk)

    def rtobj_get(self):
        return self.rt_obj
