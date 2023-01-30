import argparse
import math
import copy
from tqdm import tqdm

from code.classes import board, game
from code.algorithms import dfs_hill_climber, randomise, priority_red_car, move_cars_in_way, \
    depth_first, breadth_first, randomise_move_more_squares, priority_children

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'solves rush hour')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)",)
    parser.add_argument("output_file", help = "location output file(csv)")

    # read arguments from command line
    args = parser.parse_args()

    # create a board for the data
    # test_board = board.Board(f"data/gameboards/" + args.input_file)

    # ---------- Solve by random car movements - Branch and Bound -------------
    # nr_moves_to_solve = math.inf

    # for i in tqdm(range(1), desc="Solving boards…", ascii=False, ncols=75):
    #     test_board = board.Board(f"data/gameboards/" + args.input_file)
    #     test_game = game.Game(f"data/solutions/" + args.output_file, \
    #         test_board, randomise.random_car_move, \
    #             branch_and_bound=True, nr_moves_to_solve=nr_moves_to_solve)

    #     nr_moves_to_solve = test_game.nr_moves_to_solve

    # --------- Solve by priority red car and random car movements ------------
    nr_moves_to_solve = math.inf

    for i in tqdm(range(10000), desc="Solving boards…", ascii=False, ncols=75):
        test_board = board.Board(f"data/gameboards/" + args.input_file)

        test_game = game.Game(f"data/solutions/" + args.output_file, \
                test_board, priority_red_car.move_priority_red_car, \
                    branch_and_bound=True, nr_moves_to_solve=nr_moves_to_solve)

        nr_moves_to_solve = test_game.nr_moves_to_solve

    # ---------
    # test_board = board.Board(f"data/gameboards/" + args.input_file)
    # test_game = game.Game(f"data/solutions/" + args.output_file, \
    #     test_board, randomise_move_more_squares.random_car_move)

    # --------

    # test_board = board.Board(f"data/gameboards/" + args.input_file)
    # test_game = game.Game(f"data/solutions/" + args.output_file, \
    #     test_board, priority_children.PriorityChildren, first_search=True)

    # test_game = game.Game(f"data/solutions/" + args.output_file, \
    #     test_board, depth_first.Depth_First_Search, first_search=True)

    # test_game = game.Game(f"data/solutions/" + args.output_file, \
    #         test_board, breadth_first.BreadthFirst, first_search=True)



