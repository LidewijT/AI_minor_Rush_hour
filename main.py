import argparse
import math
import copy
from tqdm import tqdm
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from code.classes import board, game
from code.algorithms import dfs_hill_climber, randomise, priority_red_car, move_cars_in_way, \
    depth_first, breadth_first, depth_limited, randomise_move_more_squares, priority_children


if __name__ == "__main__":
    data_dls = []

    # for board_nr in ["6x6_3", "9x9_4"]:
    for board_nr in ["6x6_1", "6x6_2","6x6_3"]:
        test_board = board.Board(f"data/gameboards/" + f"Rushhour{board_nr}.csv")

        for max_depth in range(0, 1100, 20):
            print()
            print(f"Depth-limited Search, {board_nr}, with max-depth: {max_depth}")

            test_game = game.Game(f"data/solutions/" + "dfs_lim_" + str(max_depth) +"_6x6_1.csv", \
                test_board, depth_limited.Depth_Limited_Search, first_search=True, max_depth=max_depth)

            if test_game.win == True:
                data_dls.append({
                    "board": board_nr,
                    "max_depth": max_depth,
                    "number_of_states": test_game.nr_states,
                    "number_of_moves": test_game.moves_df.shape[0]
                })

            else:
                data_dls.append({
                    "board": board_nr,
                    "max_depth": max_depth,
                    "number_of_states": test_game.nr_states,
                    "number_of_moves": 0
                })

    df_data_dls = pd.DataFrame(data_dls)
    df_data_dls.to_csv("data/gameboards_different_max_depth_DLS2.csv", index=False)

    df_data_dls.plot(x='number_of_states', y='number_of_moves', kind='scatter')
    plt.xlabel('Number of States')
    plt.ylabel('Number of Moves')
    plt.show()
    plt.savefig('plot1.png')






    # print("Depth-limited Search, 9x9_5")
    # test_board = board.Board(f"data/gameboards/" + "Rushhour9x9_5.csv")
    # test_game = game.Game(f"data/solutions/" + "dls__9x9_5.csv", \
    #     test_board, depth_limited.Depth_Limited_Search, first_search=True, max_depth=3000)





    # test_board = board.Board(f"data/gameboards/" + "Rushhour9x9_6.csv")
    # print("\nBFS, 9x9_6")
    # test_game = game.Game(f"data/solutions/" + "bfs_9x9_6.csv", \
    #         test_board, breadth_first.Breadth_First_Search, first_search=True)

    # print("DFS, 12x12_7")
    # test_board = board.Board(f"data/gameboards/" + "Rushhour12x12_7.csv")
    # test_game = game.Game(f"data/solutions/" + "dfs_12x12_7.csv", \
    #     test_board, depth_first.Depth_First_Search, first_search=True)
    # print("\nBFS, 12x12_7")
    # test_game = game.Game(f"data/solutions/" + "bfs_12x12_7.csv", \
    #         test_board, breadth_first.Breadth_First_Search, first_search=True)

    # print("DFS, 12x12_7")
    # test_board = board.Board(f"data/gameboards/" + "Rushhour12x12_7.csv")
    # test_game = game.Game(f"data/solutions/" + "dfs_12x12_7.csv", \
    #     test_board, depth_first.Depth_First_Search, first_search=True)








#     # initiate variables
#     branch_and_bound_bool = False
#     first_search_bool = False
#     nr_moves_to_solve_nbr = None
#     graph_bool = False
#     runs = 1

#     # word completers
#     board_completer = WordCompleter(["Rushhour6x6_1", "Rushhour6x6_2", \
#     "Rushhour6x6_3", "Rushhour9x9_4", "Rushhour9x9_5", "Rushhour9x9_6", \
#     "Rushhour12x12_7"])

#     algorithm_completer = WordCompleter(["randomise.random_car_move", \
#     "priority_red_car.move_priority_red_car", "breath_first.Breath_first_search"\
#     , "depth_first.DepthFirst"])

#     yes_no_completer = WordCompleter(["yes", "no"])

#     # ask user for input on what to run
#     board_name = prompt("What board do you want to run?: ", \
#     completer = board_completer) + ".csv"

#     algorithm = prompt("What algorithm would you like to run? \
# choose from: \nrandom, priority random, breath first or depth first: "\
#     , completer = algorithm_completer)


#     if algorithm == "randomise.random_car_move" or \
#     algorithm == "priority_red_car.move_priority_red_car":
#         branch = prompt("Would you like to add a branch and bound heuristic \
# to your algorithm yes/no?: ", completer = yes_no_completer)
#         runs = int(input("how many iterations do you want to run?: "))

#         if branch == "yes":
#             branch_and_bound_bool = True
#             nr_moves_to_solve_nbr = math.inf

#     if algorithm == "depth_first.DepthFirst" or \
#     algorithm == "breath_first.Breath_first_search":
#         first_search_bool = True

#         if algorithm == "depth_first.DepthFirst":
#             max_depth = int(input("Give a max depth you'd like to run the \
# algorithm to: "))

#     # graph_bool = propt("Would you l", completer = yes_no_completer)
#     # if graph_bool == "yes":
#     #     png_output = input("Give a file name to save the graph to: ") + ".png"
#     #     csv_output = input("Give a file name to save the amount of moves to: ") + ".csv"

#     # else:
#     csv_output = input("Give a file name to save the made moves to: ") + ".csv"

#     # create a board for the data
#     test_board = board.Board(f"data/gameboards/" + board_name)

#     if graph_bool == False:
#         for i in tqdm(range(runs), desc="Solving boards…", ascii=False, ncols=75):
#             test_game = game.Game(f"data/solutions/" + csv_output, \
#                 test_board, eval(algorithm), first_search = first_search_bool, \
#                 branch_and_bound = branch_and_bound_bool, \
#                 nr_moves_to_solve = nr_moves_to_solve_nbr)



#     else:
#         random_moves_list = []
#         priority_moves_list = []

#         for i in tqdm(range(int(args.iterations)), desc="Solving boards…", ascii=False, ncols=75):
#             # run random algorithm
#             test_game = game.Game(f"data/solutions/" + args.output_file, \
#                 copy.deepcopy(test_board), randomise.random_car_move)

#             # append the number of moves it took to solve the board to list
#             number_of_moves_random = test_game.move_counter
#             random_moves_list.append(number_of_moves_random)

#             # run random with priority algorithm
#             test_game = game.Game(f"data/solutions/" + args.output_file, \
#                 copy.deepcopy(test_board), priority_red_car.move_priority_red_car)

#             # append the number of moves it took to solve the board to list
#             number_of_moves_prio = test_game.move_counter
#             priority_moves_list.append(number_of_moves_prio)

#         # make lists into dataframe
#         moves_to_solve_df = pd.DataFrame({'total moves random': random_moves_list, \
#         'total moves priority': priority_moves_list})

#         # save dataframe to csv
#         moves_to_solve_df.to_csv(args.output_file, index=False)

#         # plot data to histplot with kernal density estimate
#         sns.histplot(moves_to_solve_df, kde=True)
#         plt.xlabel('Total number of moves to reach winning state')
#         plt.xlim(0, 50000)
#         plt.ylim(0, 115)
#         plt.title('Arrangement of total number of moves needed to solve board 6x6_2')
#         plt.savefig(f"data/graphs/" + args.output_png)
#         plt.show()


    # # set-up parsing command line arguments
    # parser = argparse.ArgumentParser(description = 'solves rush hour')
    #
    # # adding arguments
    # parser.add_argument("input_file", help = "location input file (csv)",)
    # parser.add_argument("output_file", help = "location output file(csv)")
    #
    # # arguments for running experiments
    # # parser.add_argument("output_png", help = "location output file(png)")
    # # parser.add_argument("iterations", help = "the amount of runs you want done")
    #
    # # read arguments from command line
    # args = parser.parse_args()

    # # create a board for the data
    # test_board = board.Board(f"data/gameboards/" + board)
    #
    # test_game = game.Game(f"data/solutions/" + output_file, \
    #     test_board, algorithm, first_search = first_search_bool, \
    #     branch_and_bound = branch_and_bound_bool)

    # ---------- Solve by random car movements - Branch and Bound -------------
    # nr_moves_to_solve = math.inf

    # for i in tqdm(range(1), desc="Solving boards…", ascii=False, ncols=75):
    #     test_board = board.Board(f"data/gameboards/" + args.input_file)
    #     test_game = game.Game(f"data/solutions/" + args.output_file, \
    #         test_board, randomise.random_car_move, \
    #             branch_and_bound=True, nr_moves_to_solve=nr_moves_to_solve)

    # -------- Test random algorithm to random with priority algorithm --------
    # random_moves_list = []
    # priority_moves_list = []
    #
    # for i in tqdm(range(int(args.iterations)), desc="Solving boards…", ascii=False, ncols=75):
    #     # run random algorithm
    #     test_game = game.Game(f"data/solutions/" + args.output_file, \
    #         copy.deepcopy(test_board), randomise.random_car_move)
    #
    #     # append the number of moves it took to solve the board to list
    #     number_of_moves_random = test_game.move_counter
    #     random_moves_list.append(number_of_moves_random)
    #
    #     # run random with priority algorithm
    #     test_game = game.Game(f"data/solutions/" + args.output_file, \
    #         copy.deepcopy(test_board), priority_red_car.move_priority_red_car)
    #
    #     # append the number of moves it took to solve the board to list
    #     number_of_moves_prio = test_game.move_counter
    #     priority_moves_list.append(number_of_moves_prio)
    #
    # # make lists into dataframe
    # moves_to_solve_df = pd.DataFrame({'total moves random': random_moves_list, \
    # 'total moves priority': priority_moves_list})
    #
    # # save dataframe to csv
    # moves_to_solve_df.to_csv(args.output_file, index=False)
    #
    # # plot data to histplot with kernal density estimate
    # sns.histplot(moves_to_solve_df, kde=True)
    # plt.xlabel('Total number of moves to reach winning state')
    # plt.xlim(0, 50000)
    # plt.ylim(0, 115)
    # plt.title('Arrangement of total number of moves needed to solve board 6x6_2')
    # plt.savefig(f"data/graphs/" + args.output_png)
    # plt.show()


    # # ----------- Solve by priority red car and random car movements -----------
    # moves_to_solve_priority_df = pd.DataFrame(columns=['total moves'])
    #
    # priority_list = []
    #
    # for i in tqdm(range(100), desc="Solving boards…", ascii=False, ncols=75):
    #     test_board = board.Board(f"data/gameboards/" + args.input_file)
    #     test_game = game.Game(f"data/solutions/" + args.output_file, \
    #             test_board, priority_red_car.move_priority_red_car)
    #
    #     number_of_moves = test_game.move_counter
    #     priority_list.append(number_of_moves)
    #
    # moves_to_solve_df['total moves priority'] = priority_list
    #
    #     # move_df = pd.DataFrame([number_of_moves], columns=['total moves'], index=[i])
    #     # moves_to_solve_priority_df = pd.concat([moves_to_solve_priority_df, move_df])
    #
    # moves_to_solve_df.to_csv(args.output_file, index=False)
    #
    # # sns.histplot(moves_to_solve_priority_df, stat='percent', ax=axis[1])
    # sns.histplot(moves_to_solve_df, stat='percent')
    #
    # plt.show()


    # ------------ Solve by random car movements - Branch and Bound ------------
    # nr_moves_to_solve = math.inf
    #
    # for i in tqdm(range(1), desc="Solving boards…", ascii=False, ncols=75):
    #     test_board = board.Board(f"data/gameboards/" + args.input_file)
    #     test_game = game.Game(f"data/solutions/" + args.output_file, \
    #         test_board, randomise.random_car_move, \
    #             branch_and_bound=True, nr_moves_to_solve=nr_moves_to_solve)
    #
    #     print(f"Rush Hour was solved in {test_game.nr_moves_to_solve} moves\n")
    #
    #     nr_moves_to_solve = test_game.nr_moves_to_solve

    # --------- Solve by priority red car and random car movements ------------
    # nr_moves_to_solve = math.inf

    # for i in tqdm(range(10000), desc="Solving boards…", ascii=False, ncols=75):
    #     test_board = board.Board(f"data/gameboards/" + args.input_file)

    #     test_game = game.Game(f"data/solutions/" + args.output_file, \
    #             test_board, priority_red_car.move_priority_red_car, \
    #                 branch_and_bound=True, nr_moves_to_solve=nr_moves_to_solve)

    #     nr_moves_to_solve = test_game.nr_moves_to_solve

    # ---------
    # test_board = board.Board(f"data/gameboards/" + args.input_file)
    # test_game = game.Game(f"data/solutions/" + args.output_file, \
    #     test_board, randomise_move_more_squares.random_car_move)

    # --------

    # test_board = board.Board(f"data/gameboards/" + args.input_file)
    # test_game = game.Game(f"data/solutions/" + args.output_file, \
    #     test_board, priority_children.PriorityChildren, first_search=True)
