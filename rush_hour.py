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
        # self.position = [(row, col)]
        self.col = col
        self.row = row
        self.length = length
        self.color = color
        self.move = True

class Board():
    def __init__(self):
        self.vehicle_list = []

    def make_board(self, input_file):
        """
        Reads the csv input file and creates a board of the same grid size
        """
        # read csv
        self.gameboard_df = pd.read_csv(input_file)

        # get grid size
        name_split = input_file.split("Rushhour")[-1]
        self.grid_size = int(name_split.split("x")[0])

        # set each square on the grid to 'not occupied' (= False)
        self.occupation = np.zeros((self.grid_size, self.grid_size), dtype=bool)

        # add vehicles to list
        self.add_vehicles()

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
            self.vehicle_list.append(Vehicles(vehicle[1]['car'], \
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

    def move(self):
        # create an empty grid
        self.create_grid(self.grid_size)

        for vehicle in self.vehicle_list:
            # update position of vehicle
            if vehicle.orientation == 'H':
                # draw horizontal turned vehicles on the board
                for tiles in range(vehicle.length):
                    self.update_square(self.grid[vehicle.row][vehicle.col + tiles], vehicle.color)
                    # update the occupation of the current square
                    self.occupation[vehicle.row][vehicle.col + tiles] = True
            else:
                # draw vertical turned vehicles on the board
                for tiles in range(vehicle.length):
                    self.update_square(self.grid[vehicle.row + tiles][vehicle.col], vehicle.color)
                    # update the occupation of the current square
                    self.occupation[vehicle.row + tiles][vehicle.col] = True

        print(self.occupation)

        # plot the grid
        self.root.mainloop()

        # move cars
        # check for free squares (not occupied by vehicles)
        free_row, free_col = np.where(self.occupation == False)

        for vehicle in self.vehicle_list:
            # check if vehicle is around a free square







    def update_square(self, square, color):
        self.canvas.itemconfig(square, fill=color)

    def move_vehicles(self):
        pass

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'solves rush hour')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)")
    # parser.add_argument("output_file", help = "location output file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run board class with provided argument to create the board of the inputfile
    Board().make_board(args.input_file)
