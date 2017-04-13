import json


def gamerank_return(message):
    f = open("server/games/gamerank", "r")
    f_ = json.loads(f.read())
    f_.close()
    string = "Gamerank\n\n"
    passed = False
    for i in range(len(f_)):
        if i <= 20:
            string += str(i) + ". " + str(f_[i][0].server) + "\n"
            if f_[i][0].server.id == message.server.id:
                passed = True
        else:
            if passed:
                break
            else:
                if f_[i][0].server.id == message.server.id:
                    passed = True
    return [["text", "```" + string + "```"]]
