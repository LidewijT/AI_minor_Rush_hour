"""
Experiments what the lowest amount of moves the random and random with priority
algorith gives with the branch and bound heuristic. Outputs the smallest move set
per board and algorith to a csv
"""

import math
from tqdm import tqdm
import copy

import code.helpers.prompt_helper as ph

from ..algorithms import priority_red_car, randomise
from ..classes import board, game

# --------------------------- set variables for run ----------------------------
runs = 300
given_percentage = 0.15
algorithm_list = ["randomise.random_car_move", "priority_red_car.move_priority_red_car"]

adapted_board_list = ph.board_list[4:]
# ---------- Test random algorithm to random with priority algorithm -----------
for board_name in adapted_board_list:
    test_board = board.Board(f"data/gameboards/" + board_name + ".csv")

    for algorithm in algorithm_list:
        print()

        nr_moves_to_solve_nbr = math.inf

        print(f"running {board_name} with {algorithm} algorithm")

        csv_output = f"{board_name}_{algorithm}_{runs}_its_branched.csv"


        for i in tqdm(range(runs), desc="Solving boards…", ascii=False, ncols=75):

            test_game = game.Game(f"data/solutions/random_branch/" + csv_output, \
                copy.deepcopy(test_board), eval(algorithm), branch_and_bound = True, \
                nr_moves_to_solve = nr_moves_to_solve_nbr, percentage=given_percentage)

            if test_game.move_counter < nr_moves_to_solve_nbr:
                print(f"the new best is: {test_game.move_counter}")

            nr_moves_to_solve_nbr = test_game.move_counter
