import argparse

from tiktaktoe import Game

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='tik-tak-toe',
        description='A online version of a classic tic-tac-toe game.',
    )
    parser.add_argument(
        '-c',
        '--create',
        action='store_true',
        help='Create a new game.',
    )
    parser.add_argument(
        '-j',
        '--join',
        help='Join a game using UUID.',
    )
    args = parser.parse_args()
    game = Game()

    if args.create:
        game.new()
    else:
        game.join(args.join)

    game.loop()
