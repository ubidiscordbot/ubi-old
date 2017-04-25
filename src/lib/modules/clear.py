#Short module amiright
def main(message):
    return [["purgeText", int(message.content.split(' ', 1)[1])]]
