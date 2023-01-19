import argparse
import math
from tqdm import tqdm

from code.classes import board, game
from code.algorithms import randomise, priority_red_car, move_cars_in_way

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'solves rush hour')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)",)
    parser.add_argument("output_file", help = "location output file(csv)")

    # read arguments from command line
    args = parser.parse_args()

    # ---------- Solve by random car movements - Branch and Bound -------------
    nr_moves_to_solve = math.inf
    n = 1000

    # solve the rush hour n times and save the lowest number of moves
    for i in tqdm(range(n), desc="Solving boards…", ascii=False, ncols=75):
        # create a board for the data
        test_board = board.Board(f"data/gameboards/" + args.input_file)

        # solve board
        test_game = game.Game(f"data/solutions/" + args.output_file, \
            test_board, randomise.random_car_move, \
                branch_and_bound=True, nr_moves_to_solve=nr_moves_to_solve)

        nr_moves_to_solve = test_game.nr_moves_to_solve

        # close tkinter window
        test_board.root.destroy()