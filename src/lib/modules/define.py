from PyDictionary import PyDictionary
dictionary = PyDictionary()


def main(message):
    word = message.content.split(' ', 1)[1]
    defined = dictionary.meaning(word)
    print(defined)
    return [["text", defined]]
