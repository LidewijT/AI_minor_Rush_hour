"""
Experiments on all boards what percentage of priority movement to the red car
is the most efficient from 5 to 60 percent in steps of 5. Saves output of
total moves made as csv and a plot to pgn
"""

import math
import copy
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from ..classes import board, game
from ..algorithms import dfs_hill_climber, randomise, priority_red_car, \
move_cars_in_way, depth_first, breath_first, randomise_move_more_squares, \
depth_limited
from ..helpers import prompt_helper as ph

# --------------------------- set variables for run ----------------------------
runs = 100

# ---------- Test random algorithm to random with priority algorithm -----------
for given_percentage in range(5, 61, 5):
    for board_name in ph.board_list:
        print(f"running {board_name}, {given_percentage}%")

        output_file = f"{given_percentage}_percent_{board_name}_{runs}_its"
        output_png = f"{given_percentage}_percent_{board_name}_{runs}_its"

        random_moves_list = []
        priority_moves_list = []

        for i in tqdm(range(int(runs)), desc="Solving boards…", ascii=False, ncols=75):
            # create a board for the data
            test_board = board.Board(f"data/gameboards/" + board_name + ".csv")

            # run random algorithm
            test_game = game.Game(f"data/solutions/" + output_file + ".csv", \
                test_board, randomise.random_car_move)

            # append the number of moves it took to solve the board to list
            number_of_moves_random = test_game.move_counter
            random_moves_list.append(number_of_moves_random)

            # create a board for the data
            test_board = board.Board(f"data/gameboards/" + board_name + ".csv")

            # run random with priority algorithm
            test_game = game.Game(f"data/solutions/" + output_file + ".csv", \
                test_board, priority_red_car.move_priority_red_car, \
                percentage=given_percentage / 100)

            # append the number of moves it took to solve the board to list
            number_of_moves_prio = test_game.move_counter
            priority_moves_list.append(number_of_moves_prio)

        # make lists into dataframe
        moves_to_solve_df = pd.DataFrame({'total moves random': random_moves_list, \
        'total moves priority': priority_moves_list})

        # save dataframe to csv
        moves_to_solve_df.to_csv("data/graphs/random_priority_testing/" \
        + output_file + ".csv", index=False)

        # plot data to histplot with kernal density estimate
        sns.histplot(moves_to_solve_df, kde=True, stat = "percent")
        plt.xlabel('Total number of moves to reach winning state')
        plt.xlim(0, 220000)
        plt.ylim(0, 25)
        plt.title(f'Number of moves needed to solve\
 {board_name}\n with a priority percentage of {given_percentage}, run {runs} times')
        plt.savefig("data/graphs/random_priority_testing/" + output_png + ".png")
        plt.clf()

        print()
