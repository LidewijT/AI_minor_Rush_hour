import argparse

from code.classes import board

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'solves rush hour')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)")
    # parser.add_argument("output_file", help = "location output file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run game with provided argument
    board.Board(args.input_file)