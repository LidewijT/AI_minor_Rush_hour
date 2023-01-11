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
        # self.col = col
        # self.row = row
        self.length = length
        self.color = color
        self.move = True

        if orientation == "H":
            for tile in range(length):
                self.positions.append((row, col + tile))
        else:
            for tile in range(length):
                self.positions.append((row + tile, col))

class Board():
    def __init__(self, input_file):
        # self.vehicle_list = []
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

        # set each square on the grid to 'not occupied' (= False)
        # self.occupation = np.zeros((self.grid_size, self.grid_size))
        self.occupation = np.empty((self.grid_size, self.grid_size), dtype=str)

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

    def move(self):
        # create an empty grid
        self.create_grid(self.grid_size)

        for vehicle_name, veh_obj in self.vehicle_dict.items():
            # update position of vehicle in grid
            for row, col in veh_obj.positions:
                self.update_square(self.grid[row][col], veh_obj.color)
                # update the occupation of the current square
                self.occupation[row][col] = veh_obj.car

        print(self.occupation)

        # plot the grid
        self.root.mainloop()

        # move cars
        # check for free squares (not occupied by vehicles)
        free_row, free_col = np.where(self.occupation == '')

        for i in range(len(free_row)):
            # get combination of row and col to determine free square
            r = free_row[i]
            c = free_col[i]

            # get squares around free square
            left_square = (r, c - 1)
            right_square = (r, c + 1)
            bottom_square = (r - 1, c)
            upper_square = (r + 1, c)

            # left square
            # try:
            #     if len(self.occupation[r][c - 1]) == 1:
            print(self.vehicle_dict)
            # print(self.vehicle_list[0].car)

            # except:
            #     pass
            # for vehicle in self.vehicle_list:










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

    # run board class with provided argument
    Board(args.input_file)
