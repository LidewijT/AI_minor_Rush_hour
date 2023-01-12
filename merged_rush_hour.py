"""
In this file we will simulate the game of rush hour
"""
# import libraries
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mlc
import tkinter as tk
import random

# initiate the classes
class Vehicles():
    def __init__(self, car, orientation, col, row, length, color):
        # get attributes
        self.car = car
        self.orientation = orientation
        self.positions = []
        self.length = length
        self.color = color
        self.move = True

        # create a list of positions the vehicle occupies
        if orientation == "H":
            for tile in range(length):
                self.positions.append((row, col + tile))
        else:
            for tile in range(length):
                self.positions.append((row + tile, col))

class Board():
    def __init__(self, input_file):
        self.vehicle_dict = {}

        self.make_board(input_file)

    def make_board(self, input_file):
        """
        Reads the csv input file and creates a board of the same grid size
        """
        # read csv
        self.gameboard_df = pd.read_csv(input_file)

        # get grid size
        name_split = input_file.split("Rushhour")[-1]
        self.grid_size = int(name_split.split("x")[0])

        # create empty grid matrix
        self.occupation = np.empty((self.grid_size, self.grid_size), dtype=str)

        # add vehicles to list
        self.add_vehicles()

        # create an empty grid
        self.create_grid(self.grid_size)

        # move function
        self.move()

    def add_vehicles(self):
        """
        Create a list of all vehicles of class Vehicle() with its attributes
        """
        for vehicle in self.gameboard_df.iterrows():
            # make sure car X has always color red
            if vehicle[1]['car'] == "X":
                color_veh = "#FF0000"
            else:
                # create random hex value for vehicle color
                color_veh = ["#"+''.join([random.choice('01234566789ABCDEF') for s in range(6)])]

            # create Vehicle() and add to list
            self.vehicle_dict[vehicle[1]['car']] = (Vehicles(vehicle[1]['car'], \
                vehicle[1]['orientation'], vehicle[1]['col'] - 1, vehicle[1]['row'] - 1, \
                vehicle[1]['length'], color_veh))

    def create_grid(self, grid_size):
        width_grid = 720

        # create the main window
        self.root = tk.Tk()
        # set base for size of grid
        self.canvas = tk.Canvas(self.root, width=width_grid, height=width_grid)
        self.canvas.pack()

        # create grid
        self.grid = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                # calculate size of each square corresponding with grid size
                square = self.canvas.create_rectangle(j * (width_grid / \
                    grid_size), i * (width_grid / grid_size), (j + 1) * \
                    (width_grid / grid_size),(i + 1) * (720 / grid_size), \
                    fill='dimgrey')
                row.append(square)
            self.grid.append(row)

        # place created window at the center of the screen
        self.root.eval('tk::PlaceWindow . center')

    def update_grid(self):
        for _, veh_obj in self.vehicle_dict.items():
            # update position of vehicle in grid
            for row, col in veh_obj.positions:
                self.update_square(self.grid[row][col], veh_obj.color)
                # update the occupation of the current square
                self.occupation[row][col] = veh_obj.car

        # update the figure
        self.root.update()
        plt.pause(0.5)

    def move(self):
        # update the grid
        self.update_grid()

        # move cars
        self.checkfreesquares()

    def update_square(self, square, color):
        self.canvas.itemconfig(square, fill=color)

    def checkfreesquares(self):
        # check for free squares (not occupied by vehicles)
        free_row, free_col = np.where(self.occupation == '')

        test_amount_of_loops = 0
        for i in range(len(free_row)):
            # get combination of row and col to determine free square
            r = free_row[i]
            c = free_col[i]

            # move vehicle to the left
            # is position to the right of the
            # free square within the grid and occupied
            if c + 1 < self.grid_size and len(self.occupation[r][c + 1]) >= 1:
                current_veh = self.vehicle_dict[self.occupation[r][c + 1]]

                if current_veh.orientation == "H":
                    self.move_vehicle_back(current_veh, r, c)

            # move vehicle to the right
            # is position to the left of the
            # free square within the grid and occupied
            if c - 1 >= 0 and len(self.occupation[r][c - 1]) >= 1:
                current_veh = self.vehicle_dict[self.occupation[r][c - 1]]
                # print(current_veh.positions)

                if current_veh.orientation == "H":
                    self.move_vehicle_ahead(current_veh, r, c)

            # move vehicle up
            # is position above the free square within the grid and occupied
            if r + 1 < self.grid_size and len(self.occupation[r + 1][c]) >= 1:
                current_veh = self.vehicle_dict[self.occupation[r + 1][c]]

                if current_veh.orientation == "V":
                    self.move_vehicle_back(current_veh, r, c)

            # move vehicle down
            # is position above the free square within the grid and occupied
            if r - 1 >= 0 and len(self.occupation[r - 1][c]) >= 1:
                current_veh = self.vehicle_dict[self.occupation[r - 1][c]]

                if current_veh.orientation == "V":
                    self.move_vehicle_ahead(current_veh, r, c)

            self.update_grid()

            test_amount_of_loops += 1
            # if test_amount_of_loops >= 8:
            # 	break

        self.move()

    def move_vehicle_back(self, current_veh, r, c):
        # move vehicle backwards (left/up)
        current_veh.positions.insert(0, (r,c))
        self.occupation[current_veh.positions[-1]] = ''

        # update square back to grey ("empty")
        grey_r, grey_c = current_veh.positions[-1]
        self.update_square(self.grid[grey_r][grey_c], "dimgrey")

        current_veh.positions = current_veh.positions[:-1]
        # print(current_veh.positions)

    def move_vehicle_ahead(self, current_veh, r, c):
        # move vehicle ahead (right/down)
        current_veh.positions.append((r,c))
        # print(current_veh.positions)
        self.occupation[current_veh.positions[0]] = ''

        # update square back to grey
        grey_r, grey_c = current_veh.positions[0]
        self.update_square(self.grid[grey_r][grey_c], "dimgrey")

        current_veh.positions = current_veh.positions[1:]
        # print(current_veh.positions)

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'solves rush hour')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)")
    # parser.add_argument("output_file", help = "location output file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run board class with provided argument
    Board(args.input_file)
