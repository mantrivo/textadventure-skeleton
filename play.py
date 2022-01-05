import game

def main():
    # clear console
    print(chr(27) + "[2J")

    # load your mapfile from https://www.trizbort.io
    mygame = game.game(file="Adventure.json")
    p = game.player(mygame, language="en")
    p.play()


main()