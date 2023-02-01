import pandas as pd
import time

from ..algorithms import breadth_first, depth_first, depth_limited, \
    dfs_hill_climber, priority_children, priority_red_car, randomise

class Game:
    """
    This class is designed to solve the Rush Hour gameboard using the input
    algorithm. The class has different methods for running the algorithm,
    depending on the parameters passed in. A dataframe is used to store all
    moves to get to the winning state, which is exported to a CSV file when the
    game is won.
    """
    def __init__(self, output_file, test_board, algorithm, \
        branch_and_bound = False, nr_moves_to_solve = None, first_search =
            False, percentage = None, create_csv = True, max_depth = None):
        """
        Initializes the attributes for the class including the output file,
        the test board, and the algorithm to be used. It also has additional
        parameters such as branch_and_bound which is a heuristic, and
        first_search which is used for a specific type of algorithm.
        """
        # attributes
        self.output_file = output_file
        self.test_board = test_board
        self.occupation_board = test_board.board
        self.algorithm = algorithm
        self.max_depth = max_depth
        self.create_csv = create_csv

        # keep track of all moves
        self.moves_df = pd.DataFrame(columns=['car name', 'move'])
        self.move_counter = 0

        # start solving with algorithm
        if branch_and_bound == True:
            self.nr_moves_to_solve = nr_moves_to_solve
            self.run_branch_and_bound()

        elif first_search == True:
            self.run_first_search()

        else:
            self.percentage = percentage
            self.run()

    def run_branch_and_bound(self):
        """
        This method is used when the branch_and_bound parameter is set to
        true. It uses the algorithm passed in to make moves on the board until
        the red car reaches the exit or the move counter reaches the value of
        nr_moves_to_solve. Furtermore, it keeps track of all moves made in a
        DataFrame.
        """
        # keep moving cars until red car is at exit
        while self.win_check() == False and \
            self.move_counter < self.nr_moves_to_solve:

            self.move_counter += 1

            # make a move
            self.occupation_board, vehicle, direction = self.algorithm(
                self.test_board,
                self.occupation_board
            )

            # save the move
            self.append_move_to_DataFrame(vehicle, direction)


    def run_first_search(self):
        """
        This method is used when the first_search parameter is set to true.
        It uses the algorithm passed in to make moves on the board.
        It gets the move dataframe created by the algorithm and export it to a
        csv file.
        """
        # start timer
        start_time = time.time()

        # run algorithm
        result = self.algorithm(self.test_board, max_depth=self.max_depth)

        # stop timer
        end_time = time.time()

        # get results
        self.elapsed_time = end_time - start_time
        self.win = result.won
        self.nr_states = len(result.children_parent_dict)

        if self.win == True:
            self.moves_df = result.moves_df

            print(f"Number of states {self.nr_states}")
            print(f"Rush Hour was solved in {self.moves_df.shape[0]} moves")
            print(f"finished in: {self.elapsed_time} seconds")

            if self.create_csv == True:
                # finalize into csv file
                self.output_maker()

        else:
            print("No solution found")

    def run(self):
        """
        This method runs the algorithm until the board is at winning position,
        while saving each move into a dataframe. In the end, the dataframe is
        exported to a csv file if set to True.
        """
        while self.win_check() == False:
            self.move_counter += 1

            # make a move
            self.occupation_board, vehicle, direction = self.algorithm(
                self.test_board,
                self.occupation_board
            )

            # save move
            self.append_move_to_DataFrame(vehicle, direction)


    def win_check(self):
        """
        Checks whether the red car is positioned at the exit tile (=winning
        position). If so, it creates a csv file of the move dataframe if set to
        True and return True. Otherwise, it returns False.
        """
        if self.occupation_board[self.test_board.exit_tile] == \
            self.test_board.red_car:
            # board is in a winning position
            self.nr_moves_to_solve = self.move_counter

            if self.create_csv == True:
                # create csv file of the moves made
                self.output_maker()

            return True

        else:
            # board is not in a winning position
            return False

    def append_move_to_DataFrame(self, vehicle, direction):
        """
        Saves the move in a dataframe.
        """
        # append move to DataFrame
        move_df = pd.DataFrame([[vehicle.car, direction]],
            columns=['car name', 'move']
        )
        self.moves_df = pd.concat([self.moves_df, move_df])

    def compress_DataFrame(self):
        """
        If one vehicle was moved multiple times in a row,
        compress them to one move of multiple tiles
        """
        pass

    def output_maker(self):
        """
        Exports the dataframe of moves to a csv file.
        """
        self.moves_df.to_csv(self.output_file, index=False)
