"""
Creates the board and allows it to update it.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mlc
import tkinter as tk

from ..colors import cnames
from .vehicle import Vehicles


class Board():
    def __init__(self, input_file):
        self.move_counter = 0

        self.vehicle_dict = {}
        # self.parent_occupation = np.zeros((self.grid_size, self.grid_size))

        self.load_vehicles(input_file)
        self.create_board(input_file)

    def load_vehicles(self, input_file):
        """
        Load all vehicles into a dictionary as object Vehicles.
        """
        self.gameboard_df = pd.read_csv(input_file)

        # add vehicles to dictionary as objects
        self.add_vehicles()

    def add_vehicles(self):
        """
        Create a dictionary with the vehicle names as key and the corresponding
        object with the vehicle's attributes as value.
        """
        # set counter for iterating through colorlist
        i = 0
        for vehicle in self.gameboard_df.iterrows():

            # make sure car X has always color red
            if vehicle[1]['car'] == "X":
                color_veh = "#FF0000"

                # store the number of the red car
                self.red_car = vehicle[0] + 1

            else:
                # retrieve hex value for vehicle color
                colorl_list = list(cnames.items())
                color_veh = colorl_list[i][1]

                i += 1

                if i >= len(colorl_list):
                    # start at the beginning of the colorlist if all colors have
                    # been used
                    i = 0

            # create Vehicle() and add to list
            self.vehicle_dict[vehicle[0] + 1] = (Vehicles(vehicle[1]['car'], \
                vehicle[1]['orientation'], vehicle[1]['col'] - 1, vehicle[1]['row'] - 1, \
                vehicle[1]['length'], color_veh, vehicle[0] + 1))

    def create_board(self, input_file):
        """
        Creates a rush hour board using the intitial state given in the input
        file.
        """
        # get grid size
        self.grid_size = self.get_gridsize(input_file)

        # determine the exit tile
        self.exit_tile = ((self.grid_size - 1) // 2, self.grid_size - 1)

        # create grid matrix to keep track of occupied squares
        self.occupation = np.zeros((self.grid_size, self.grid_size))

        # create an empty board
        # self.create_grid(self.grid_size)

        # place vehicles onto the board
        self.update_board()

    def get_gridsize(self, input_file):
        """
        Returns the gridsize of the input file by using its file name
        """
        name_split = input_file.split("Rushhour")[-1]
        grid_size = int(name_split.split("x")[0])

        return grid_size

    def create_grid(self, grid_size):
        """
        Takes the gridsize as input and creates an empty board.
        """
        # set size for window on screen
        graph_size = 720

        # create the main window
        self.root = tk.Tk()
        # set base for size of window
        self.canvas = tk.Canvas(self.root, width=graph_size, height=graph_size)
        self.canvas.pack()

        # create empty board
        self.grid = []

        for i in range(grid_size):
            row = []

            for j in range(grid_size):
                # calculate size of each square corresponding with grid size
                square = self.canvas.create_rectangle(j * (graph_size / \
                    grid_size), i * (graph_size / grid_size), (j + 1) * \
                    (graph_size / grid_size),(i + 1) * (graph_size / grid_size), \
                    fill='dimgrey')
                row.append(square)

            self.grid.append(row)

        # place created window at the center of the screen
        self.root.eval('tk::PlaceWindow . center')

    def update_board(self):
        """
        Updates the board using the positions of all vehicles. Also updates the
        occupation matrix to keep track of occupied squares.
        """
        for car_number, veh_obj in self.vehicle_dict.items():
            for row, col in veh_obj.positions:
                # update position of vehicle in grid
                # self.update_square(self.grid[row][col], veh_obj.color)
                # update the occupation of the current square
                self.update_occupation(row, col, car_number)

        # # update the figure window
        # self.root.update()

    def update_occupation(self, row, col, car_number):
        """
        Updates the occupation with the vehicle name of the current square.
        """
        self.occupation[row][col] = car_number

    def update_square(self, square, color):
        """
        Takes position (row, column) of the square and updates it to the input
        color on the board.
        """
        self.canvas.itemconfig(square, fill=color)

    def get_free_squares(self):
        """
        Checks where the occumation matrix is not filled with a car. Returns an
        numpy array for both row an column positions in which the indices
        matches the free squares.
        """
        free_row, free_col = np.where(self.occupation == 0)

        return free_row, free_col

    def empty_square(self, vehicle, direction):

        """
        Updates a square back to default color (=dimgrey)
        """
        # update square the vehicle moved away from back to grey ("empty")
        # grey_r, grey_c = vehicle.positions[direction]
        # self.update_square(self.grid[grey_r][grey_c], "dimgrey")


    def car_move(self, direction, r, c):
        # move vehicle to the left respectively from free square
        if c + 1 < self.grid_size and \
        self.occupation[r][c + 1] >= 1 and direction == "left" and \
        self.vehicle_dict[self.occupation[r][c + 1]].orientation == "H":
            neighbouring_veh = self.vehicle_dict[self.occupation[r][c + 1]]

            self.move_vehicle_back(neighbouring_veh, r, c)
            return neighbouring_veh

        # move vehicle to the right respectively from free square
        elif c - 1 >= 0 and \
        self.occupation[r][c - 1] >= 1 and direction == "right" and \
        self.vehicle_dict[self.occupation[r][c - 1]].orientation == "H":
            neighbouring_veh = self.vehicle_dict[self.occupation[r][c - 1]]

            self.move_vehicle_ahead(neighbouring_veh, r, c)
            return neighbouring_veh

        # move vehicle to the up respectively from free square
        elif r + 1 < self.grid_size \
        and self.occupation[r + 1][c] >= 1 and direction == "up" and \
        self.vehicle_dict[self.occupation[r + 1][c]].orientation == "V":
            neighbouring_veh = self.vehicle_dict[self.occupation[r + 1][c]]

            self.move_vehicle_back(neighbouring_veh, r, c)
            return neighbouring_veh

        # move vehicle to the move respectively from free square
        elif r - 1 >= 0 and self.occupation[r - 1][c] >= 1 \
        and direction == "down" and \
        self.vehicle_dict[self.occupation[r - 1][c]].orientation == "V":
            neighbouring_veh = self.vehicle_dict[self.occupation[r - 1][c]]

            self.move_vehicle_ahead(neighbouring_veh, r, c)
            return neighbouring_veh

    def move_vehicle_back(self, vehicle, r, c):
        """
        Takes a vehicle object and updates its position towards the given row
        and column. Updates the occupation matrix and the new vehicle positions.
        """
        # move vehicle backwards (left/up)
        vehicle.positions.insert(0, (r,c))
        self.occupation[vehicle.positions[-1]] = 0

        # update square the vehicle moved away from back to grey ("empty")
        self.empty_square(vehicle, -1)

        # update the positions the vehicle is at
        vehicle.positions = vehicle.positions[:-1]
        self.update_board()

    def move_vehicle_ahead(self, vehicle, r, c):
        """
        Moves input vehicle 'ahead' (either to the right or down) based on the
        input row and column. Updates the occupation matrix and the left square
        back to grey.
        """
        # move vehicle ahead (right/down)
        vehicle.positions.append((r,c))
        self.occupation[vehicle.positions[0]] = 0

        # update square the vehicle moved away from back to grey ("empty")
        self.empty_square(vehicle, 0)

        # update the positions the vehicle is at
        vehicle.positions = vehicle.positions[1:]
        self.update_board()
