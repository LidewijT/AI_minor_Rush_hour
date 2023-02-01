import math
from tqdm import tqdm
import os

from code.classes import board, game
import code.helpers.prompt_helper as ph

from code.classes import board, game, visualisation
from code.algorithms import breadth_first, depth_first, depth_limited, \
depth_hill_climber, depth_priority_children, priority_red_car, randomise

if __name__ == "__main__":
    # ---------------------- initiate starting variables -----------------------
    # these are standart variables to run the program and can be changed
    # during the prompts
    branch_and_bound_bool = False
    first_search_bool = False
    max_depth = None
    runs = 1

    # ------------------- ask user for input on what to run --------------------
    # ask user what board to run
    board_name = ph.board_prompt()

    # ask user if they want to run a visualisation
    visualisation_bool = ph.visualisation_bool_prompt()

    # if so, ask what input file of moves they want to use
    if visualisation_bool in {"yes", "y"}:
        moves_input = ph.moves_input_prompt()

    else:
        # ask what algorithm they want to run
        algorithm = ph.algorithm_prompt()

        # check if the algorith is a random based algorith
        if algorithm in {"randomise.random_car_move",
        "priority_red_car.move_priority_red_car"}:

            # ask user if they want to add the branch and bound heuristic
            branch = ph.branch_prompt()

            # if branch and bound is wanted, set variables
            if branch in {"yes", "y"}:
                branch_and_bound_bool = True

            # ask how many runs the user wants to run the algorithm for
            runs = ph.runs_prompt()

        else:
            first_search_bool = True

            if algorithm == "depth_limited.Depth_Limited_Search":
                # ask for the max depth the user wants to apply
                max_depth = ph.max_depth_prompt()

        # ask what file the user wants to save the output to
        csv_output = ph.csv_output_prompt()

    # prints a line in terminal to signify the switch from setup to running
    width = os.get_terminal_size().columns
    print()
    print("-" * width)
    print("Thank you for your input")

    # ----------------- Run the game with the given arguments ------------------
    # the user wants to see a visualisation of moves
    if visualisation_bool in {"yes", "y"}:
        # create a board for the data
        test_board = board.Board(f"data/gameboards/" + board_name)

        print("Initiating visualisation: \n")

        visualisation.Visualisation("data/gameboards/" + board_name, \
        "data/solutions/" + moves_input)

    # the user wants to use an algorithm to solve a rushhour board
    else:
        print("\nNow solving rush hour: \n")

        for i in tqdm(range(runs), desc="Solving boards…", ascii=False, ncols=75):
            # in case branch and bound is run
            nr_moves_to_solve_nbr = math.inf

            # create a board for the data
            test_board = board.Board(f"data/gameboards/" + board_name)

            # run
            test_game = game.Game(f"data/solutions/" + csv_output, \
                test_board, eval(algorithm), first_search = first_search_bool, \
                branch_and_bound = branch_and_bound_bool, \
                nr_moves_to_solve = nr_moves_to_solve_nbr)

            nr_moves_to_solve_nbr = test_game.move_counter

        print()

        if test_game.win == True:
            if algorithm not in {"randomise.random_car_move",
            "priority_red_car.move_priority_red_car"}:
                print(f"Number of visited states to find a solution: {self.nr_states}")

            print(f"Rush Hour was solved in {test_game.moves_df.shape[0]} moves")

        else:
            print("No solution found")

    print("-" * width)
