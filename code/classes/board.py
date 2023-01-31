"""
Creates the board and allows it to update it.
"""
import numpy as np
import pandas as pd
from .vehicle import Vehicles


class Board():
    """
    This class is used to create and steer the gameboard of the Rush Hour game
    in the inputfile. It consists of a grid of squares, where each square can
    hold a (part of a) vehicle or be empty. The class provides methods to place
    and move vehicles and check for valid moves.
    """
    def __init__(self, input_file):
        """
        Takes as input a csv file and creates the starting state of the Rush
        Hour gameboard by loading all vehicles into a dictionary as Vehicles
        objects, creating a rush hour occupation board using the given input
        file and determining the exit tile for the red car.
        """
        self.vehicle_dict = {}

        self.load_vehicles(input_file)
        self.create_board(input_file)

    def load_vehicles(self, input_file):
        """
        Reads the input file as a CSV file and loads all the vehicles into a
        dataframe. It then calls the 'add_vehicles' method to add each vehicle
        to the dictionary as objects.
        """
        # get all vehicles into a dataframe
        self.gameboard_df = pd.read_csv(input_file)

        # add vehicles to dictionary as objects
        self.add_vehicles()

    def add_vehicles(self):
        """
        Create a dictionary with the vehicle numbers as key and the
        corresponding object with the vehicle's attributes as values.
        """
        for vehicle in self.gameboard_df.iterrows():
            # save the number of car X (red car) for later purposes
            if vehicle[1]['car'] == "X":
                # store the number of the red car
                self.red_car = vehicle[0] + 1


            # create Vehicle() and add to dictionary
            self.vehicle_dict[vehicle[0] + 1] = (Vehicles(vehicle[1]['car'], \
                vehicle[1]['orientation'], vehicle[1]['col'] - 1, vehicle[1]['row'] - 1, \
                vehicle[1]['length'], vehicle[0] + 1))

    def create_board(self, input_file):
        """
        Creates an empty board with the determine grid size, sets the exit tile, 
        and calls the create_initial_board method to place vehicles onto the
        empty board for its initial state.
        """
        # get grid size
        self.grid_size = self.get_gridsize(input_file)

        # determine the exit tile
        self.exit_tile = ((self.grid_size - 1) // 2, self.grid_size - 1)

        # create grid matrix to keep track of occupied squares
        self.board = np.zeros((self.grid_size, self.grid_size))

        # place vehicles onto the occupation board for its initial state
        self.create_initial_board()

    def get_gridsize(self, input_file):
        """
        Returns the gridsize of the input file by using its file name.
        """
        name_split = input_file.split("Rushhour")[-1]
        grid_size = int(name_split.split("x")[0])

        return grid_size

    def create_initial_board(self):
        """
        Creates the starting state of the Rush Hour board using the empty
        board to place all vehicles using their positions.
        vehicles.
        """
        for car_number, veh_obj in self.vehicle_dict.items():
            for row, col in veh_obj.positions:
                # update the occupation of the current square in the board
                self.board[row][col] = car_number

    def get_free_squares(self, occupation_board):
        """
        Checks where the occumation board is not filled with a car (square=0).
        Returns an numpy array for both row an column positions in which the
        indices matche into the coordinate of the free squares.
        """
        free_row, free_col = np.where(occupation_board == 0)

        return free_row, free_col

    def get_vehicle(self, occupation_board, r, c):
        """
        Gets the vehicle number and object for a given row and column position
        in the occupation board.
        """
        self.vehicle_number = occupation_board[r][c]
        self.vehicle_obj = self.vehicle_dict[self.vehicle_number]

    def update_occupation_board(self, occupation_board, r, c, sign):
        """
        Updates the occupation board for the current vehicle by updating the
        'head' of the vehicle to the free square and the 'tail' of the vehicle
        back to a free square.
        """
        veh_length = self.vehicle_obj.length

        # update the 'head' of the vehicle to the free square (r, c)
        occupation_board[r][c] = self.vehicle_number

        # update the 'tail' of the horizontal vehicle back to a free square
        if self.vehicle_obj.orientation == "H":
            col = c + veh_length if sign == '+' else c - veh_length
            occupation_board[r][col] = 0

        # update the 'tail' of the vertical vehicle back to a free square
        else:
            row = r + veh_length if sign == '+' else r - veh_length
            occupation_board[row][c] = 0

        return occupation_board

    def car_move(self, occupation_board, direction, r, c):
        """
        Check or the valid moves in a given direction. If valid, it moves the
        vehicle by updating the occupation board and returning the updated
        board.
        """
        # move vehicle left to free square
        if c + 1 < self.grid_size and \
        occupation_board[r][c + 1] >= 1 and direction == "left" and \
        self.vehicle_dict[occupation_board[r][c + 1]].orientation == "H":
            # get vehicle and update occupation board
            self.get_vehicle(occupation_board, r, c + 1)
            occupation_board = self.update_occupation_board(occupation_board, \
                r, c, '+')

        # move vehicle right to free square
        elif c - 1 >= 0 and \
        occupation_board[r][c - 1] >= 1 and direction == "right" and \
        self.vehicle_dict[occupation_board[r][c - 1]].orientation == "H":
            # get vehicle and update occupation board
            self.get_vehicle(occupation_board, r, c - 1)
            occupation_board = self.update_occupation_board(occupation_board, \
                r, c, '-')

        # move vehicle up to free square
        elif r + 1 < self.grid_size \
        and occupation_board[r + 1][c] >= 1 and direction == "up" and \
        self.vehicle_dict[occupation_board[r + 1][c]].orientation == "V":
            # get vehicle and update occupation board
            self.get_vehicle(occupation_board, r + 1, c)
            occupation_board = self.update_occupation_board(occupation_board, \
                r, c, '+')

        # move vehicle down respectively from free square
        elif r - 1 >= 0 and occupation_board[r - 1][c] >= 1 \
        and direction == "down" and \
        self.vehicle_dict[occupation_board[r - 1][c]].orientation == "V":
            # get vehicle and update occupation board
            self.get_vehicle(occupation_board, r - 1, c)
            occupation_board = self.update_occupation_board(occupation_board, \
                r, c, '-')

        # no vehicles able to move to the free square
        else:
            return False, occupation_board

        # return the moved vehicle with the updated board
        return self.vehicle_obj, occupation_board