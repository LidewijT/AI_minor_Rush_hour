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
from colors import cnames

# increase maximum recursion depth to prevent RecursionError
import sys
sys.setrecursionlimit(10**9)

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
    def __init__(self, input_file, output_file):
        self.move_counter = 0
        self.vehicle_dict = {}
        self.output_file = output_file
        self.moves_df = pd.DataFrame(columns=['car name', 'move'])

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
        self.occupation = np.zeros((self.grid_size, self.grid_size))

        # add vehicles to list
        self.add_vehicles()

        # create an empty grid
        self.create_grid()

        # move function
        self.move()

    def add_vehicles(self):
        """
        Create a list of all vehicles of class Vehicle() with its attributes
        """
        i = 0
        for vehicle in self.gameboard_df.iterrows():

            # make sure car X has always color red
            if vehicle[1]['car'] == "X":
                color_veh = "#FF0000"

                # store the number of the red car
                self.red_car = vehicle[0] + 1

            else:
                # retrieve hex value for vehicle color
                color_list = list(cnames.items())
                color_veh = color_list[i][1]

                i += 1
                if i >= len(color_list):
                    i = 0

            # create Vehicle() and add to list
            self.vehicle_dict[vehicle[0] + 1] = (Vehicles(vehicle[1]['car'], \
                vehicle[1]['orientation'], vehicle[1]['col'] - 1, vehicle[1]['row'] - 1, \
                vehicle[1]['length'], color_veh))

    def create_grid(self):
        graph_size = 720

        # create the main window
        self.root = tk.Tk()
        # set base for size of grid
        self.canvas = tk.Canvas(self.root, width=graph_size, height=graph_size)
        self.canvas.pack()

        # create grid
        self.grid = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                # calculate size of each square corresponding with grid size
                square = self.canvas.create_rectangle(j * (graph_size / \
                    self.grid_size), i * (graph_size / self.grid_size), (j + 1) * \
                    (graph_size / self.grid_size),(i + 1) * (graph_size / self.grid_size), \
                    fill='dimgrey')
                row.append(square)
            self.grid.append(row)

        # place created window at the center of the screen
        self.root.eval('tk::PlaceWindow . center')

    def update_grid(self):
        for car_number, veh_obj in self.vehicle_dict.items():
            # print(car_number, veh_obj.positions)
            # update position of vehicle in grid
            for row, col in veh_obj.positions:
                self.update_square(self.grid[row][col], veh_obj.color)
                # update the occupation of the current square
                self.occupation[row][col] = car_number

        # update the figure
        self.root.update()
        plt.pause(0.01)

    def move(self):
        # update the grid
        self.update_grid()

        #check if the winning position is reached
        winning_condition = self.win_check()
        self.move_counter += 1

        # to test wether the output maker works
        if self.move_counter >= 5:
            winning_condition = True
            self.output_maker()

        # move cars only if winning condtion is not reached
        if winning_condition == False:# and self.move_counter < 5:
            self.checkfreesquares()



    def update_square(self, square, color):
        self.canvas.itemconfig(square, fill=color)

    def checkfreesquares(self):
        # determine which squares are free
        free_row, free_col = np.where(self.occupation == 0)

        # pick random free square until car moves
        pick_free_square = True

        while pick_free_square == True:

            # pick random index for free square
            idx_free_square = random.randint(0, len(free_row) - 1)

            # get combination of row and col to determine position free square
            r = free_row[idx_free_square]
            c = free_col[idx_free_square]

            # delete chosen free square to not pick again
            free_row = np.delete(free_row, idx_free_square)
            free_col = np.delete(free_col, idx_free_square)

            # list for random squares around free square
            surrounding_squares = ["left", "right", "up", "down"]

            # pick until all surroundings squares have been tried
            for _ in range(4):
                # pick random surrounding square
                surr_square = random.choice(surrounding_squares)

                # delete from list to not pick again
                surrounding_squares.remove(surr_square)

                """try the surrounding squares"""

                # move vehicle to the left
                # if position to the right of the
                # free square is within the grid and occupied
                # and the orientation of this vehicle is horizontal
                if c + 1 < self.grid_size and \
                self.occupation[r][c + 1] >= 1 and surr_square == "left":

                    neighbouring_veh = self.vehicle_dict[self.occupation[r][c + 1]]

                    if neighbouring_veh.orientation == "H":
                        self.move_vehicle_back(neighbouring_veh, r, c)

                        # append move to DataFrame
                        self.append_move_to_DataFrame(neighbouring_veh, "left")

                        pick_free_square = False
                        break

                # move vehicle to the right
                # if position to the left of the
                # free square is within the grid and occupied
                # and the orientation of this vehicle is horizontal
                elif c - 1 >= 0 and \
                self.occupation[r][c - 1] >= 1 and surr_square == "right":
                    neighbouring_veh = self.vehicle_dict[self.occupation[r][c - 1]]

                    if neighbouring_veh.orientation == "H":
                        self.move_vehicle_ahead(neighbouring_veh, r, c)

                        # append move to DataFrame
                        self.append_move_to_DataFrame(neighbouring_veh, "right")

                        pick_free_square = False
                        break

                # move vehicle up if position below the
                # free square is within the grid and occupied
                # and the orientation of this vehicle is vertical
                elif r + 1 < self.grid_size \
                and self.occupation[r + 1][c] >= 1 and surr_square == "up":
                    neighbouring_veh = self.vehicle_dict[self.occupation[r + 1][c]]

                    if neighbouring_veh.orientation == "V":
                        self.move_vehicle_back(neighbouring_veh, r, c)

                        # append move to DataFrame
                        self.append_move_to_DataFrame(neighbouring_veh, "up")

                        pick_free_square = False
                        break

                # move vehicle down if position above the
                # free square is within the grid and occupied
                # and the orientation of this vehicle is vertical
                elif r - 1 >= 0 and self.occupation[r - 1][c] >= 1 \
                and surr_square == "down":
                    neighbouring_veh = self.vehicle_dict[self.occupation[r - 1][c]]

                    if neighbouring_veh.orientation == "V":
                        self.move_vehicle_ahead(neighbouring_veh, r, c)

                        # append move to DataFrame
                        self.append_move_to_DataFrame(neighbouring_veh, "down")

                        pick_free_square = False
                        break

        self.move()

    def move_vehicle_back(self, vehicle, r, c):
        # move vehicle backwards (left/up)
        vehicle.positions.insert(0, (r,c))
        self.occupation[vehicle.positions[-1]] = 0

        # update square the vehicle moved away from back to grey ("empty")
        grey_r, grey_c = vehicle.positions[-1]
        self.update_square(self.grid[grey_r][grey_c], "dimgrey")

        vehicle.positions = vehicle.positions[:-1]

    def move_vehicle_ahead(self, vehicle, r, c):
        # move vehicle ahead (right/down)
        vehicle.positions.append((r,c))
        self.occupation[vehicle.positions[0]] = 0

        # update square the vehicle moved away from back to grey ("empty")
        grey_r, grey_c = vehicle.positions[0]
        self.update_square(self.grid[grey_r][grey_c], "dimgrey")

        vehicle.positions = vehicle.positions[1:]

    def append_move_to_DataFrame(self, vehicle, direction):
        # append move to DataFrame
        move_df = pd.DataFrame([[vehicle.car, direction]], \
        columns=['car name', 'move'])
        self.moves_df = pd.concat([self.moves_df, move_df])

    def win_check(self):

        winning_c = self.grid_size - 1
        winning_r = (self.grid_size - 1) // 2

        if self.occupation[(winning_r, winning_c)] == self.red_car:
            print('dikke win broer')
            print(f"Je hebt gewonnen na {self.move_counter} zetten")
            output_maker()
            return True

        else:
            return False

        # if self.occupation[(winning_r, winning_c)] >= 1:
        #     occupating_vehicle = self.occupation[(winning_r, winning_c)]
        #
        #     if (self.vehicle_dict[occupating_vehicle]).car == "X":
        #         print('dikke win broer')
        #         print(f"Je hebt gewonnen na {self.move_counter} zetten")
        #         output_maker()
        #         return True
        #
        #     else:
        #         return False




    def output_maker(self):
        # this function saves a dataframe of moves to a csv file
        self.moves_df.to_csv(self.output_file, index=False)

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = 'solves rush hour')

    # adding arguments
    parser.add_argument("input_file", help = "location input file (csv)")
    parser.add_argument("output_file", help = "location output file(csv)")


    # read arguments from command line
    args = parser.parse_args()

    # run board class with provided argument
    Board(args.input_file, args.output_file)
