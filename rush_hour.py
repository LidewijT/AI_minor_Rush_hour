"""
In this file we will simulate the game of rush hour
"""
# import libraries
import argparse
import numpy as np
import pandas as pd


# initiate the classes
class Vehicles():
    def __init__(self, car, orientation, col, row, length):
        self.car = car
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length

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
        grid_size = int(name_split.split("x")[0])
        print(grid_size)

        # add vehicles
        self.add_vehicles()

    def add_vehicles(self):
        """
        Create a list of all vehicles on the board with its characteristics
        """
        for vehicle in self.gameboard_df.iterrows():
            self.vehicle_list.append(Vehicles(vehicle[1]['car'], vehicle[1]['orientation'], vehicle[1]['col'], vehicle[1]['row'], vehicle[1]['length']))




if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'to be determined')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)")
    # parser.add_argument("output_file", help = "location output file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run board class with provided argument to creaded the board of the inputfile
    Board().make_board(args.input_file)
