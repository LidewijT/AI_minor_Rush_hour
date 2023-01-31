import argparse
import math
import copy
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from code.classes import board, game
import code.helpers.prompt_helper as ph
from code.algorithms import dfs_hill_climber, randomise, priority_red_car, \
move_cars_in_way, depth_first, breath_first, randomise_move_more_squares


if __name__ == "__main__":
    # ---------------------- initiate starting variables -----------------------
    branch_and_bound_bool = False
    first_search_bool = False
    nr_moves_to_solve_nbr = None
    graph_bool = False
    runs = 1

    # ------------------- ask user for input on what to run --------------------
    board_name = ph.board_prompt()

    visualisation_bool = ph.visualisation_bool_prompt()

    if visualisation_bool in {"yes", "y"}:
        moves_input = moves_input_prompt()

    else:
        algorithm = ph.algorithm_prompt()

        if algorithm == "randomise.random_car_move" or \
        algorithm == "priority_red_car.move_priority_red_car":
            branch = ph.branch_prompt()
            runs = ph.runs_prompt()

            if branch in {"yes", "y"}:
                branch_and_bound_bool = True
                nr_moves_to_solve_nbr = math.inf

        if algorithm == "depth_first.DepthFirst_search" or \
        algorithm == "breath_first.Breath_first_search":
            first_search_bool = True

            # if algorithm == "depth_first.DepthFirst":
            #     max_depth = ph.max_depth_prompt()

        csv_output = ph.csv_output_prompt()

    # ----------------- Run the game with the given arguments ------------------
    # create a board for the data
    test_board = board.Board(f"data/gameboards/" + board_name)

    if graph_bool not in {"yes", "y"}:
        for i in tqdm(range(runs), desc="Solving boards…", ascii=False, ncols=75):
            test_game = game.Game(f"data/solutions/" + csv_output, \
                test_board, eval(algorithm), first_search = first_search_bool, \
                branch_and_bound = branch_and_bound_bool, \
                nr_moves_to_solve = nr_moves_to_solve_nbr)

    else:
        Visualisation("data/gameboards/" + board_name, \
        "data/solutions/" + csv_output)


    # else:
    #     random_moves_list = []
    #     priority_moves_list = []
    #
    #     for i in tqdm(range(runs), desc="Solving boards…", ascii=False, ncols=75):
    #         # run random algorithm
    #         test_game = game.Game(f"data/solutions/" + csv_output, \
    #             copy.deepcopy(test_board), randomise.random_car_move)
    #
    #         # append the number of moves it took to solve the board to list
    #         number_of_moves_random = test_game.move_counter
    #         random_moves_list.append(number_of_moves_random)
    #
    #         # run random with priority algorithm
    #         test_game = game.Game(f"data/solutions/" + csv_output, \
    #             copy.deepcopy(test_board), priority_red_car.move_priority_red_car)
    #
    #         # append the number of moves it took to solve the board to list
    #         number_of_moves_prio = test_game.move_counter
    #         priority_moves_list.append(number_of_moves_prio)
    #
    #     # make lists into dataframe
    #     moves_to_solve_df = pd.DataFrame({'total moves random': random_moves_list, \
    #     'total moves priority': priority_moves_list})
    #
    #     # save dataframe to csv
    #     moves_to_solve_df.to_csv(csv_output, index=False)
    #
    #     # plot data to histplot with kernal density estimate
    #     sns.histplot(moves_to_solve_df, kde=True)
    #     plt.xlabel('Total number of moves to reach winning state')
    #     plt.xlim(0, 50000)
    #     plt.ylim(0, 115)
    #     plt.title('Arrangement of total number of moves needed to solve board 6x6_2')
    #     plt.savefig(f"data/graphs/" + png_output)
    #     plt.show()
