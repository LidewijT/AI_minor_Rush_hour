import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
import argparse
import random
from ..helpers.colors import color_list, big_color_list
from matplotlib.colors import ListedColormap

class Visualisation():
    def __init__(self, board_csv, moves_csv):
        # store the file paths for the board and moves csv files
        self.board_csv = board_csv
        self.moves_csv = moves_csv
        # initiate move counter
        self.move_counter = 0
        #import color_lists
        self.own_colors = ListedColormap(color_list)
        self.big_color_list = big_color_list
        # call the run method to start the visualization
        self.run()

    def run(self):
        # read in the board and moves data from the csv files
        self.read_csvs()
        # get the grid size based on the board csv file name
        self.get_gridsize()
        # create the initial grid and display it
        self.create_grid()
        # animate the moves
        self.move_cars()

    def change_positions(self):
        self.df_board['col'] += 1
        self.df_board['row'] += 1

    def read_csvs(self):
        # read in the board and moves csv files using pandas
        self.df_board = pd.read_csv(self.board_csv)
        self.df_moves = pd.read_csv(self.moves_csv)

    def get_gridsize(self):
        """
        Returns the grid size of the input file by using its file name
        """
        # split the board csv file name to get the grid size
        name_split = self.board_csv.split("Rushhour")[-1]
        self.grid_size = int(name_split.split("x")[0])

    def letter_to_number(self, letter):
        """
        Converts a letter to a unique number so that every car always has the
        same number to be used in the color list.
        """
        if letter == 'X':
            return 1
        elif letter == 'grey':
            return 5
        else:
            return ord(letter) - ord('A') + 2

    def pick_random_color(self):
        return random.choice(self.big_color_list)

    def create_grid(self, break_time = 0.2):
        # create an empty numpy array to represent the grid
        self.grid = np.zeros((self.grid_size, self.grid_size))

        # set the outer row and column to a constant value representing grey color
        self.grid[0, :] = self.grid[-1, :] = self.grid[:, 0] = self.grid[:, -1] = -1

        # populate the grid with the cars and their orientations
        for i,(_, row) in enumerate(self.df_board.iterrows()):
            car, orientation, col, row, length = row

            # place the car horizontally
            if orientation == 'H':
                for j in range(length):
                    # assign the numerical value of the car (determined by
                    # letter_to_number function) to each grid cell occupied by the car
                    self.grid[row-1][col-1+j] = self.letter_to_number(car)

            # place the car vertically
            else:
                for j in range(length):
                    # assign the numerical value of the car (determined by
                    # letter_to_number function) to each grid cell occupied by the car
                    self.grid[row-1+j][col-1] = self.letter_to_number(car)

        # clear the previous plot
        plt.clf()
        # plot the grid using the specified colormap (self.own_colors) and with the specified color range (0-max value in the grid)
        plt.imshow(self.grid, cmap= self.own_colors,
        vmin = 0, vmax = self.grid.max())
        # change background color
        plt.gcf().set_facecolor('grey')
        # add a title to the plot, indicating the name of the board and the current move number
        plt.title(f'Visualisation of {self.board_csv} - Move: {self.move_counter}')
        # turn off the X and Y axis
        plt.axis("off")
        # show the plot but do not block execution of the code
        plt.show(block = False)
        # pause execution for the specified amount of time (break_time)
        plt.pause(break_time)

    def move_cars(self):
        """
        The method loops through each row in the "df_moves" dataframe and updates the car's position
        based on the direction specified.
        """
        for _,row in self.df_moves.iterrows():
            # unpacking the car and direction from the current row
            car, direction = row
            # finding the row in "df_board" dataframe for the specified car
            vehicle_row = self.df_board.loc[self.df_board['car'] == car]

            #update move_counter when a move happens
            self.move_counter += 1

            # moving the car based on the direction
            if direction == "left":
                self.update_board(car, 'col', -1)

            elif direction == "right":
                self.update_board(car, 'col', 1)

            elif direction == "up":
                self.update_board(car, 'row', -1)

            else:
                self.update_board(car, 'row', 1)

    def update_board(self, car, axis, plus_or_minus):
        # update the position of the car on the dataframe
        self.df_board.loc[self.df_board['car'] == car, axis] += plus_or_minus

        # regenerate the grid with the updated car position
        self.create_grid()
