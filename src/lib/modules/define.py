from PyDictionary import PyDictionary
dictionary = PyDictionary()
types = ["Noun", "Verb", "Adjective", "Adverb"]

def main(message):
    word = message.content.split(' ', 1)[1]
    defined = dictionary.meaning(word)
    print(defined)
    return [["text", "[**Dictionary**] " + defined[list(defined.keys())[0]][0]]]
