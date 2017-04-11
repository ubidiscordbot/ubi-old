import random


def main():
    flip_ = random.randint(1, 2)
    if flip_ == 1:
        return [["fileKeep", "server/assets/Tails.png"]]
    elif flip_ == 2:
        return [["fileKeep", "server/assets/Heads.png"]]
