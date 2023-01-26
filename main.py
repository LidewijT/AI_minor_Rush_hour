import argparse
import math
import copy
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from code.classes import board, game
from code.algorithms import randomise, randomise2, priority_red_car, breath_first

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

    # --------------------- Solve by random car movements ----------------------
    # moves_to_solve_df = pd.DataFrame(columns=['total moves random'])

    # figure, axis = plt.subplots(1, 2)
    # print(axis)

    random_moves_list = []
    priority_moves_list = []

    for i in tqdm(range(10), desc="Solving boards…", ascii=False, ncols=75):
        # random algorithm
        test_board = board.Board(f"data/gameboards/" + args.input_file)
        test_game = game.Game(f"data/solutions/" + args.output_file, \
            test_board, randomise.random_car_move)

        number_of_moves_random = test_game.move_counter
        random_moves_list.append(number_of_moves_random)
        # move_df = pd.DataFrame([number_of_moves], columns=['total moves random'], index=[i])
        # moves_to_solve_df = pd.concat([moves_to_solve_df, move_df])

        # random with priority algorithm
        test_board = board.Board(f"data/gameboards/" + args.input_file)
        test_game = game.Game(f"data/solutions/" + args.output_file, \
                test_board, priority_red_car.move_priority_red_car)

        number_of_moves_prio = test_game.move_counter
        priority_moves_list.append(number_of_moves_prio)

        moves_to_solve_df = pd.DataFrame({'total moves random': random_moves_list, 'total moves priority': priority_moves_list})    # moves_to_solve_df['total moves priority'] = priority_list

    print(moves_to_solve_df)
    moves_to_solve_df.to_csv(args.output_file, index=False)

    sns.histplot(moves_to_solve_df, kde=True)#, color = ['blue', 'green'])#, stat='percent')

    plt.xlabel('Total number of moves to reach winning state')
    # plt.ylabel('Percentage this amount of moves was made')
    plt.xlim(0,50000)
    plt.ylim(0,115)
    plt.title('Arrangement of total number of moves needed to solve board 6x6_2')
    plt.show()

    # moves_to_solve_df.to_csv(args.output_file, index=False)

    # sns.histplot(moves_to_solve_random_df, stat='percent', ax=axis[0])
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


    # -- Solve by priority red car and random car movements - Branch and Bound--
    # nr_moves_to_solve = math.inf
    #
    # for i in tqdm(range(100000), desc="Solving boards…", ascii=False, ncols=75):
    #     test_board = board.Board(f"data/gameboards/" + args.input_file)
    #
    #     test_game = game.Game(f"data/solutions/" + args.output_file, \
    #             test_board, priority_red_car.move_priority_red_car, \
    #                 branch_and_bound=True, nr_moves_to_solve=nr_moves_to_solve)
    #
    #     nr_moves_to_solve = test_game.nr_moves_to_solve


    # -------------------- Solve by breath first algorithm ---------------------
    # test_game = game.Game(f"data/solutions/" + args.output_file, \
    #     test_board, breath_first = True) #breath_first.breath_first_search,
