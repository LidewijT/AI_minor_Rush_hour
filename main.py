import argparse
import math
import copy
from tqdm import tqdm

from code.classes import board, game
from code.algorithms import randomise, randomise2

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'solves rush hour')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)",)
    parser.add_argument("output_file", help = "location output file(csv)")

    # read arguments from command line
    args = parser.parse_args()

    # create a board for the data
    test_board = board.Board(f"data/gameboards/" + args.input_file)

    # ---------- Solve by random car movements - Branch and Bound -------------
    nr_moves_to_solve = math.inf

    for i in tqdm(range(1000), desc="Solving boards…", ascii=False, ncols=75):
        test_game = game.Game(f"data/solutions/" + args.output_file, \
            copy.deepcopy(test_board), randomise.random_car_move, \
                branch_and_bound=True, nr_moves_to_solve=nr_moves_to_solve)

        nr_moves_to_solve = test_game.nr_moves_to_solve




    # game.Game(f"data/solutions/" + args.output_file, test_board, \
    # randomise2.system_move)
