import math
import copy
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from code.classes import board, game
from code.algorithms import dfs_hill_climber, randomise, priority_red_car, \
move_cars_in_way, depth_first, breath_first, randomise_move_more_squares, \
depth_limited

# --------------------------- set variables for run ----------------------------
# board_name = "Rushhour6x6_2"
# output_file = "test"
# output_png = "test"
runs = 100

board_list = ["Rushhour6x6_3"]#["Rushhour6x6_1", "Rushhour6x6_2", "Rushhour6x6_3", "Rushhour9x9_4", \
# "Rushhour9x9_5", "Rushhour9x9_6", "Rushhour12x12_7"]

# ---------- Test random algorithm to random with priority algorithm -----------
for given_percentage in range(5, 61, 5):
    for board_name in board_list:
        print(f"running {board_name}, {given_percentage}%")

        output_file = f"{given_percentage}_percent_{board_name}_{runs}_its"
        output_png = f"{given_percentage}_percent_{board_name}_{runs}_its"

        random_moves_list = []
        priority_moves_list = []

        # create a board for the data
        # test_board = board.Board(f"data/gameboards/" + board_name + ".csv")

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
        plt.xlim(0, 350000)
        plt.ylim(0, 25)
        plt.title(f'Number of moves needed to solve\
 {board_name}\n with a priority percentage of {given_percentage}, run {runs} times')
        plt.savefig("data/graphs/random_priority_testing/" + output_png + ".png")
        plt.clf()

        print()

plt.show()