"""
Creates initial board from input file.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mlc
import tkinter as tk
import random
from ..colors import cnames

from .vehicle import Vehicles
from ..algorithms import randomise

class Board():
    def __init__(self, input_file, output_file, algorithm):
        self.move_counter = 0
        self.output_file = output_file

        self.vehicle_dict = {}
        # create dataframe to keep track of each move
        self.moves_df = pd.DataFrame(columns=['car name', 'move'])

        self.load_vehicles(input_file)
        self.create_board(input_file)
        self.move()

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
                vehicle[1]['length'], color_veh))

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
        self.create_grid(self.grid_size)

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
                self.update_square(self.grid[row][col], veh_obj.color)
                # update the occupation of the current square
                self.update_occupation(row, col, car_number)

        # update the figure window
        self.root.update()

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

    def move(self):
        self.move_counter += 1

        # to test wether the output maker works
        # if self.move_counter >= 5:
        #     winning_condition = True
        #     self.output_maker()

        # move cars only if winning condtion is not reached
        if self.win_check() == False:# and self.move_counter < 5:
            # check for free squares on the board to move to
            self.free_row, self.free_col = self.get_free_squares()

            # make a random vehicle move to a free square
            self.random_car_move()

            # update the board with the new vehicle movement
            self.update_board()

            plt.pause(0.05)

            # make another move
            self.move()

    def get_free_squares(self):
        """
        Checks where the occumation matrix is not filled with a car. Returns an
        numpy array for both row an column positions in which the indices
        matches the free squares.
        """
        free_row, free_col = np.where(self.occupation == 0)

        return free_row, free_col

    def random_car_move(self):
        """
        Picks a random vehicle to move.
        """
        # pick random free square until vehicle moves
        pick_free_square = True

        while pick_free_square == True:
            # get the position of a randomly chosen free square
            r, c = self.random_free_square()

            # self.load_vehicles
            # list for random squares around free square
            self.surrounding_squares = ["left", "right", "up", "down"]

            # pick until all surroundings squares have been tried
            for _ in range(4):
                # choose a random surrounding square
                surr_square = self.random_surrounding_square()

                # move vehicle to the left respectively from free square
                if c + 1 < self.grid_size and \
                self.occupation[r][c + 1] >= 1 and surr_square == "left":
                    neighbouring_veh = self.vehicle_dict[self.occupation[r][c + 1]]

                    # only move if the orientation of the vehicle is horizontal
                    if neighbouring_veh.orientation == "H":
                        self.move_vehicle_back(neighbouring_veh, r, c)

                        # append move to DataFrame
                        self.append_move_to_DataFrame(neighbouring_veh, "left")

                        pick_free_square = False
                        break

                # move vehicle to the right respectively from free square
                elif c - 1 >= 0 and \
                self.occupation[r][c - 1] >= 1 and surr_square == "right":
                    neighbouring_veh = self.vehicle_dict[self.occupation[r][c - 1]]

                    # only move if the orientation of the vehicle is horizontal
                    if neighbouring_veh.orientation == "H":
                        self.move_vehicle_ahead(neighbouring_veh, r, c)

                        # append move to DataFrame
                        self.append_move_to_DataFrame(neighbouring_veh, "right")

                        pick_free_square = False
                        break

                # move vehicle to the up respectively from free square
                elif r + 1 < self.grid_size \
                and self.occupation[r + 1][c] >= 1 and surr_square == "up":
                    neighbouring_veh = self.vehicle_dict[self.occupation[r + 1][c]]

                    # only move if the orientation of the vehicle is vertical
                    if neighbouring_veh.orientation == "V":
                        self.move_vehicle_back(neighbouring_veh, r, c)

                        # append move to DataFrame
                        self.append_move_to_DataFrame(neighbouring_veh, "up")

                        pick_free_square = False
                        break

                # move vehicle to the move respectively from free square
                elif r - 1 >= 0 and self.occupation[r - 1][c] >= 1 \
                and surr_square == "down":
                    neighbouring_veh = self.vehicle_dict[self.occupation[r - 1][c]]

                    # only move if the orientation of the vehicle is vertical
                    if neighbouring_veh.orientation == "V":
                        self.move_vehicle_ahead(neighbouring_veh, r, c)

                        # append move to DataFrame
                        self.append_move_to_DataFrame(neighbouring_veh, "down")

                        pick_free_square = False
                        break

    def random_free_square(self):
        """
        Picks a random free square and returns its position. Deletes it from the
        free square list to prevent it to not chose it again.
        """
        # pick random index for free square
        idx_free_square = random.randint(0, len(self.free_row) - 1)

        # get combination of row and col to determine position free square
        random_row = self.free_row[idx_free_square]
        random_col = self.free_col[idx_free_square]

        # delete chosen free square to not pick again
        self.free_row = np.delete(self.free_row, idx_free_square)
        self.free_col = np.delete(self.free_col, idx_free_square)

        return random_row, random_col

    def random_surrounding_square(self):
        """
        Chooses a random surrounding square from a list and returns this.
        """
        # pick random surrounding square
        surr_square = random.choice(self.surrounding_squares)
        # delete from list to not pick again
        self.surrounding_squares.remove(surr_square)

        return surr_square

    def move_vehicle_back(self, vehicle, r, c):
        """
        Takes a vehicle object and updates its position based on the gives row
        and column. Updates the occupation matrix and the new vehicle positions.
        """
        # move vehicle backwards (left/up)
        vehicle.positions.insert(0, (r,c))
        self.occupation[vehicle.positions[-1]] = 0

        # update square the vehicle moved away from back to grey ("empty")
        self.empty_square(vehicle, -1)

        # update the positions the vehicle is at
        vehicle.positions = vehicle.positions[:-1]

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

    def empty_square(self, vehicle, direction):
        """
        Updates a square back to default color (=dimgrey)
        """
        # update square the vehicle moved away from back to grey ("empty")
        grey_r, grey_c = vehicle.positions[direction]
        self.update_square(self.grid[grey_r][grey_c], "dimgrey")

    def append_move_to_DataFrame(self, vehicle, direction):
        """
        Saves the move in a datafram.
        """
        # append move to DataFrame
        move_df = pd.DataFrame([[vehicle.car, direction]], \
        columns=['car name', 'move'])
        self.moves_df = pd.concat([self.moves_df, move_df])

    def win_check(self):
        """
        Checks whether the red car is positioned at the exit tile (=winning
        position). If so, end the game, print the number of moves needed to
        solve, create a csv file of the move dataframe and return True.
        Otherwise, return False.
        """
        if self.occupation[self.exit_tile] == self.red_car:
            print('dikke win broer')
            print(f"Je hebt gewonnen na {self.move_counter} zetten")
            self.output_maker()
            return True

        else:
            return False

    def output_maker(self):
        """
        Exports the dataframe of moves to a csv file.
        """
        self.moves_df.to_csv(self.output_file, index=False)