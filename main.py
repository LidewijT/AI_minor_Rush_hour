import math
from tqdm import tqdm

from code.classes import board, game
import code.helpers.prompt_helper as ph
from code.algorithms import dfs_hill_climber, randomise, priority_red_car, \
    depth_first, depth_limited, breadth_first



if __name__ == "__main__":
    # ---------------------- initiate starting variables -----------------------
    branch_and_bound_bool = False
    first_search_bool = False
    nr_moves_to_solve_nbr = None
    graph_bool = False
    max_depth = None
    runs = 1

    # ------------------- ask user for input on what to run --------------------
    # # ask user if they want to run an experiment
    # experiment_bool = ph.experiment_bool_prompt()
    #
    # if experiment_bool in {"yes", "y"}:
    #     exp.run()
    #
    # else:
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
        print(algorithm)

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
        elif algorithm in {"breadth_first.Breadth_First_Search", \
        "depth_first.Depth_First_Search", "depth_limited.Depth_Limited_Search"}:
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
        print("\nNow solving rush hour: \n")

        for i in tqdm(range(runs), desc="Solving boards…", ascii=False, ncols=75):

            test_game = game.Game(f"data/solutions/" + csv_output, \
                test_board, eval(algorithm), first_search = first_search_bool, \
                branch_and_bound = branch_and_bound_bool, \
                nr_moves_to_solve = nr_moves_to_solve_nbr)
