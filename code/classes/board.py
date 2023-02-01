import numpy as np
import pandas as pd

from .vehicle import Vehicles

class Board():
    """
    This class is used to create and steer the gameboard of the Rush Hour game
    in the inputfile. It consists of a grid of squares, where each square can
    hold (a part of) a vehicle or be empty. The class provides methods to place
    and move vehicles, and check for valid moves.
    """
    def __init__(self, input_file):
        """
        Takes as input a csv file and creates the starting state of the Rush
        Hour gameboard by loading all vehicles into a dictionary as Vehicles
        objects, creating a rush hour occupation board using the given input
        file and determining the exit tile for the red car.
        """
        self.vehicle_dict = {}

        # initialise the vehicles and gameboard
        self.load_vehicles(input_file)
        self.create_board(input_file)

    def load_vehicles(self, input_file):
        """
        Reads the input file as a CSV file and loads all the
        vehicles into a dataframe. Then, it calls the 'add_vehicles' method to
        add each vehicle to the dictionary as objects.
        """
        # get all vehicles into a dataframe
        self.gameboard_df = pd.read_csv(input_file)

        # add vehicles to dictionary as objects
        self.add_vehicles()

    def add_vehicles(self):
        """
        Creates a dictionary with generated vehicle numbers as key
        and has as value the corresponding object with the vehicle's attribute.
        """
        for vehicle in self.gameboard_df.iterrows():
            if vehicle[1]['car'] == "X":
                # store the number of car X (red car) to make it easy to find
                self.red_car = vehicle[0] + 1

            # create Vehicle() for value and add to dictionary with generated
            # number from index as key
            self.vehicle_dict[vehicle[0] + 1] = (Vehicles
                (vehicle[1]['car'],
                vehicle[1]['orientation'],
                vehicle[1]['col'] - 1,
                vehicle[1]['row'] - 1,
                vehicle[1]['length'],
                vehicle[0] + 1)
            )

    def create_board(self, input_file):
        """
        Creates an empty board with the determine grid size, sets
        the exit tile, and calls the create_initial_board method to place
        vehicles onto the empty board for its starting state.
        """
        # get grid size
        self.grid_size = self.get_gridsize(input_file)

        # determine the exit tile for the red car
        self.exit_tile = ((self.grid_size - 1) // 2, self.grid_size - 1)

        # create grid matrix to keep track of occupied squares by vehicles
        self.board = np.zeros((self.grid_size, self.grid_size))

        # place vehicles onto the occupation board for its starting state
        self.create_initial_board()

    def get_gridsize(self, input_file):
        """
        Returns the gridsize of the input file by using its file name. This has
        as format Rushhournxn_m.csv, where n is the gridsize and m the number of
        the board.
        """
        # get last part of filename
        name_split = input_file.split("Rushhour")[-1]
        grid_size = int(name_split.split("x")[0])

        return grid_size

    def create_initial_board(self):
        """
        Creates the starting state of the Rush Hour board using the empty board
        to place all vehicles using their starting positions.
        """
        # loop over all vehicles and their positions
        for car_number, veh_obj in self.vehicle_dict.items():
            for row, col in veh_obj.positions:
                # update the occupation of the indexed square in the board
                self.board[row][col] = car_number

    def get_free_squares(self, occupation_board):
        """
        Checks where the occupation board is not filled with a car (square=0).
        Returns an numpy array for both row an column positions in which the
        indices match into the coordinates of the free squares.
        """
        free_row, free_col = np.where(occupation_board == 0)

        return free_row, free_col

    def get_vehicle(self, occupation_board, r, c):
        """
        Gets the vehicle number and object for a given row and column position
        in the occupation board and stores it in a variable.
        """
        self.vehicle_number = occupation_board[r][c]
        self.vehicle_obj = self.vehicle_dict[self.vehicle_number]

    def update_occupation_board(self, occupation_board, r, c, sign):
        """
        Updates the occupation board for the current vehicle by updating its
        'head' to the free square and its 'tail' back to a free square.
        """
        veh_length = self.vehicle_obj.length

        # update the 'head' of the vehicle to the free square (r, c)
        occupation_board[r][c] = self.vehicle_number

        # update the 'tail' of a horizontal vehicle back to a free square
        if self.vehicle_obj.orientation == "H":
            col = c + veh_length if sign == '+' else c - veh_length
            occupation_board[r][col] = 0

        # update the 'tail' of a vertical vehicle back to a free square
        else:
            row = r + veh_length if sign == '+' else r - veh_length
            occupation_board[row][c] = 0

        return occupation_board

    def car_move(self, occupation_board, direction, r, c):
        """
        Checks if a move is valid in a given direction. If valid, it moves the
        vehicle by updating the occupation board and returns the updated board.
        """
        # move vehicle left to the free square
        if c + 1 < self.grid_size and \
            occupation_board[r][c + 1] >= 1 and direction == "left" and \
            self.vehicle_dict[occupation_board[r][c + 1]].orientation == "H":
            # get position of vehicle
            pos_veh = (r, c + 1)
            # get mathematical sign for updating occupation board
            math_sign = "+"

            # get vehicle and update occupation board
            # self.get_vehicle(occupation_board, r, c + 1)
            # occupation_board = self.update_occupation_board(occupation_board, \
            #     r, c, '+')

        # move vehicle right to free square
        elif c - 1 >= 0 and \
            occupation_board[r][c - 1] >= 1 and direction == "right" and \
            self.vehicle_dict[occupation_board[r][c - 1]].orientation == "H":
            # get position of vehicle
            pos_veh = (r, c - 1)
            # get mathematical sign for updating occupation board
            math_sign = "-"

            # get vehicle and update occupation board
            # self.get_vehicle(occupation_board, r, c - 1)
            # occupation_board = self.update_occupation_board(occupation_board, \
            #     r, c, '-')

        # move vehicle up to free square
        elif r + 1 < self.grid_size \
            and occupation_board[r + 1][c] >= 1 and direction == "up" and \
            self.vehicle_dict[occupation_board[r + 1][c]].orientation == "V":
            # get position of vehicle
            pos_veh = (r + 1, c)
            # get mathematical sign for updating occupation board
            math_sign = "+"

            # get vehicle and update occupation board
            # self.get_vehicle(occupation_board, r + 1, c)
            # occupation_board = self.update_occupation_board(occupation_board, \
            #     r, c, '+')

        # move vehicle down respectively from free square
        elif r - 1 >= 0 and \
            occupation_board[r - 1][c] >= 1 and direction == "down" and \
            self.vehicle_dict[occupation_board[r - 1][c]].orientation == "V":
            # get position of vehicle
            pos_veh = (r - 1, c)
            # get mathematical sign for updating occupation board
            math_sign = "-"

            # # get vehicle and update occupation board
            # self.get_vehicle(occupation_board, r - 1, c)
            # occupation_board = self.update_occupation_board(occupation_board, \
            #     r, c, '-')

        # no vehicles able to move to the free square
        else:
            return False, occupation_board

        # get vehicle and update occupation board
        self.get_vehicle(occupation_board, pos_veh[0], pos_veh[1])
        occupation_board = self.update_occupation_board(
            occupation_board,
            r,
            c,
            math_sign
        )

        # return the moved vehicle with the updated board
        return self.vehicle_obj, occupation_board