import argparse
import sys

from code.classes import board, game
from code.algorithms import randomise

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'solves rush hour')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)",)
    parser.add_argument("output_file", help = "location output file(csv)")

    # read arguments from command line
    args = parser.parse_args()

    # increase maximum recursion depth to prevent RecursionError
    sys.setrecursionlimit(10**9)

    # create a board for the data
    test_board = board.Board(f"data/gameboards/" + args.input_file)

    # --------------------- Solve by random car movements ---------------------
    game.Game(f"data/solutions/" + args.output_file, test_board, \
        randomise.random_car_move)
