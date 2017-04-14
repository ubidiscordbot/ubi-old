def main(message):
    vote = message.content.split(' ', 1)[1]
    return [["textPoll", vote]]
