"""
Solves rush hour with the given algorithm
"""
import pandas as pd
import matplotlib.pyplot as plt
import time

from ..algorithms import randomise, priority_red_car, move_cars_in_way, depth_first, breadth_first

class Game:
    def __init__(self, output_file, test_board, algorithm, \
        branch_and_bound = False, nr_moves_to_solve = None, first_search =
            False):
        """
        It initializes the attributes for the class including the output file,
        the test board, and the algorithm to be used. It also has additional
        parameters such as branch_and_bound which is a heuristic, and
        first_search which is used for a specific type of algorithm.
        """
        # attributes
        self.output_file = output_file
        self.test_board = test_board
        self.occupation_board = test_board.occupation
        self.algorithm = algorithm

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
            self.run()

    def run_branch_and_bound(self):
        """
        This function is used when the branch_and_bound parameter is set to true.
        It uses the algorithm passed in to make moves on the board until the red
        car reaches the exit or the move counter reaches the value of
        nr_moves_to_solve. Furtermore, it keeps track of all moves made in a
        DataFrame.
        """
        # keep moving cars until red car is at exit
        while self.win_check() == False and \
            self.move_counter < self.nr_moves_to_solve:
            self.move_counter += 1

            self.occupation_board, vehicle, direction = self.algorithm(self.test_board, self.occupation_board)

            # make a move
            self.append_move_to_DataFrame(vehicle, direction)

            # update the board with the new vehicle movement
            # self.test_board.update_board()

    def run_first_search(self):
        """
        This function is used when the first_search parameter is set to true.
        It uses the algorithm passed in to make moves on the board.
        It gets the move dataframe created by the algorithm and export it to a
        csv file.
        """
        # start timer
        start_time = time.time()

        print("Start algorithm...")

        # get the move dataframe created by the algorithm
        self.moves_df = self.algorithm(self.test_board).moves_df

        # stop timer
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Rush Hour was solved in {self.moves_df.shape[0]} moves\n")
        print(f"finished in: {elapsed_time} seconds")

        # finalize into output
        self.output_maker()

    def run(self):
        while self.win_check() == False:
            self.move_counter += 1

            # make a move
            # print("\nstart move")
            self.occupation_board, vehicle, direction = self.algorithm(self.test_board, self.occupation_board)
            # print(f"move made\n")

            # save move
            self.append_move_to_DataFrame(vehicle, direction)

            # update the board with the new vehicle move
            # self.test_board.update_board()
<<<<<<< HEAD
            # plt.pause(0.4)
=======
            plt.pause(0.4)
            # print(test_board.occupation)
            # save movement
            # self.append_move_to_DataFrame(vehicle, direction)

            # # update the board with the new vehicle movement
            # self.test_board.update_board()

            # plt.pause(0.1)

    def run_branch_and_bound(self):
        # keep moving cars until red car is at exit
        while self.win_check() == False and \
            self.move_counter < self.nr_moves_to_solve:
            self.move_counter += 1

            # make a move
            vehicle, direction = self.algorithm(self.test_board)

            # save movement
            self.append_move_to_DataFrame(vehicle, direction)

            # update the board with the new vehicle movement
            self.test_board.update_board()


    def append_move_to_DataFrame(self, vehicle, direction):
        """
        Saves the move in a dataframe.
        """
        # append move to DataFrame
        move_df = pd.DataFrame([[vehicle.car, direction]], columns=['car name', 'move'])
        self.moves_df = pd.concat([self.moves_df, move_df])
>>>>>>> main

    def win_check(self):
        """
        Checks whether the red car is positioned at the exit tile (=winning
        position). If so, end the game, print the number of moves needed to
        solve, create a csv file of the move dataframe and return True.
        Otherwise, return False.
        """
        if self.test_board.occupation[self.test_board.exit_tile] == self.test_board.red_car:
            self.nr_moves_to_solve = self.move_counter

            # self.output_maker()

            return True

        else:
            return False

    def append_move_to_DataFrame(self, vehicle, direction):
        """
        Saves the move in a dataframe.
        """
        # append move to DataFrame
        move_df = pd.DataFrame([[vehicle.car, direction]], columns=['car name', 'move'])
        self.moves_df = pd.concat([self.moves_df, move_df])

    def compress_DataFrame(self):
        """
        If one vehicle was moved multiple times in a row,
        compress them to one move of multiple tiles
        """

    def output_maker(self):
        """
        Exports the dataframe of moves to a csv file.
        """
        self.moves_df.to_csv(self.output_file, index=False)
