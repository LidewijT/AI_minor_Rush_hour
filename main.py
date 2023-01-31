import math
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from code.classes import board, game
import code.helpers.prompt_helper as ph
from code.algorithms import dfs_hill_climber, randomise, priority_red_car, \
move_cars_in_way, depth_first, breath_first, randomise_move_more_squares, \
depth_limited


if __name__ == "__main__":
    # ---------------------- initiate starting variables -----------------------
    branch_and_bound_bool = False
    first_search_bool = False
    nr_moves_to_solve_nbr = None
    graph_bool = False
    max_depth = None
    runs = 1

    # ------------------- ask user for input on what to run --------------------
    # ask user what board to run
    board_name = ph.board_prompt()

    # ask user if they want to run a visualisation
    visualisation_bool = ph.visualisation_bool_prompt()

    # if so, ask what input file of moves they want to use
    if visualisation_bool in {"yes", "y"}:
        moves_input = moves_input_prompt()

    else:
        # ask what algorithm they want to run
        algorithm = ph.algorithm_prompt()

        if algorithm in {"randomise.random_car_move", \
        "priority_red_car.move_priority_red_car"}:

            # ask user if they want to add the branch and bound heuristic
            branch = ph.branch_prompt()

            # if branch and bound is wanted, set variables
            if branch in {"yes", "y"}:
                branch_and_bound_bool = True
                nr_moves_to_solve_nbr = math.inf

            # ask how many runs the user wants to run the algorithm for
            runs = ph.runs_prompt()

        # check if an first search algorithm is used
        elif algorithm in {"depth_first.DepthFirst_search", \
        "breath_first.Breath_first_search", "depth_limited.Depth_Limited_Search"}:
            first_search_bool = True

            if algorithm == "depth_limited.Depth_Limited_Search":
                # ask for the max depth the user wants to apply
                max_depth = ph.max_depth_prompt()

        # ask what file the user wants to save the output to
        csv_output = ph.csv_output_prompt()


    # ----------------- Run the game with the given arguments ------------------
    print("\nThank you for your input")

    # create a board for the data
    test_board = board.Board(f"data/gameboards/" + board_name)

    # the user wants to see a visualisation of moves
    if visualisation_bool in {"yes", "y"}:
        print("Initiating visualisation: \n")

        Visualisation("data/gameboards/" + board_name, \
        "data/solutions/" + csv_output)

    # the user wants to use an algorithm to solve a rushhour board
    else:
        print("Now solving rush hour: \n")

        for i in tqdm(range(runs), desc="Solving boards…", ascii=False, ncols=75):
            test_game = game.Game(f"data/solutions/" + csv_output, \
                test_board, eval(algorithm), first_search = first_search_bool, \
                branch_and_bound = branch_and_bound_bool, \
                nr_moves_to_solve = nr_moves_to_solve_nbr)
