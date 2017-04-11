import os
import json


def form_new(list):
    old_list = list
    new_values = []
    for i in list:
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


def main_stats(message):
    f_ = open("server/plusplus/" + str(message.server.id) + ".json", "r")
    f = json.loads(f_.read())
    finalString = 'Name' + " " * 14 + "Credits" + "\n\n"
    n = form_new(f)
    n.reverse()
    num = 0
    for i in n:
        num += 1
        multi = 18 - len(i[0])
        finalString += str(num) + ". " + i[0] + " " * multi + str(i[1]) + "\n"
    f_.close()
    return [["text", "```" + finalString + "```"]]


def main_alter(message):
    solved = False
    f = open("server/plusplus/" + str(message.server.id) + ".json", "r")
    s = json.loads(f.read())
    f.close()
    f = open("server/plusplus/" + str(message.server.id) + ".json", "w")
    x = list(message.content)
    x.pop(0)
    x.pop(0)
    x.pop(0)
    y = ''.join(x)
    if message.author.name == y:
        f.write(json.dumps(s))
        f.close()
        return [["text", "```Nice try " + y.lower() + "!```"]]
    elif message.server.get_member_named(y) == None:
        f.write(json.dumps(s))
        f.close()
        return [["text", "```Looks like " + y.lower() + " is not a member of the server :/```"]]
    else:
        i = 0
        while i <= len(s) - 1:
            try:
                if y in s[i]:
                    if message.content[1] == "+":
                        s[i][1] += 1
                        f.write(json.dumps(s))
                        f.close()
                        return [["text", "```" + y + " just earned a point!```"]]
                    elif message.content[1] == "-":
                        s[i][1] -= 1
                        f.write(json.dumps(s))
                        f.close()
                        return [["text", "```" + y + " just lost a point.```"]]
                    solved = True
                    break
            except TypeError:
                pass
            i += 1
        if not solved:
            if message.content[1] == "+":
                s.append([y, 1])
                f.write(json.dumps(s))
                f.close()
                return [["text", "```" + y + " just earned a point!```"]]
            elif message.content[1] == "-":
                s.append([y, -1])
                f.write(json.dumps(s))
                f.close()
                return [["text", "```" + y + " just lost a point.```"]]
