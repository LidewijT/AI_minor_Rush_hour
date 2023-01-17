"""
Lukt niet want veel returnen anders:
vehicle_dict, occupation, move_df, movement car
Help
"""

import random
import numpy as np

def random_free_square(row, col):
        """
        Picks a random free square and returns its position. Deletes it from the
        free square list to prevent it to not chose it again.
        """
        # pick random index for free square
        idx_square = random.randint(0, len(row) - 1)

        # get combination of row and col to determine position free square
        random_row = row[idx_square]
        random_col = col[idx_square]

        # delete chosen free square to not pick again
        row = np.delete(row, idx_square)
        col = np.delete(col, idx_square)

        return row, col, random_row, random_col

def random_surrounding_square(squares):
        """
        Chooses a random surrounding square from a list and returns this.
        """
        # pick random surrounding square
        surr_square = random.choice(squares)
        # delete from list to not pick again
        squares.remove(surr_square)

        return surr_square, squares

def random_car_move(free_row, free_col, grid_size, occupation, vehicle_dict):
        """
        Picks a random vehicle to move.
        """
        # pick random free square until vehicle moves
        pick_free_square = True

        while pick_free_square == True:
            # get the position of a randomly chosen free square
            free_row, free_col, r, c = random_free_square(free_row, free_col)

            # load_vehicles
            # list for random squares around free square
            surrounding_squares = ["left", "right", "up", "down"]

            # pick until all surroundings squares have been tried
            for _ in range(4):
                # choose a random surrounding square
                surr_square, surrounding_squares = random_surrounding_square(surrounding_squares)

                # move vehicle to the left respectively from free square
                if c + 1 < grid_size and \
                occupation[r][c + 1] >= 1 and surr_square == "left":
                    neighbouring_veh = vehicle_dict[occupation[r][c + 1]]

                    # only move if the orientation of the vehicle is horizontal
                    if neighbouring_veh.orientation == "H":
                        move_vehicle_back(neighbouring_veh, r, c)

                        # append move to DataFrame
                        append_move_to_DataFrame(neighbouring_veh, "left")

                        pick_free_square = False
                        break

                # move vehicle to the right respectively from free square
                elif c - 1 >= 0 and \
                occupation[r][c - 1] >= 1 and surr_square == "right":
                    neighbouring_veh = vehicle_dict[occupation[r][c - 1]]

                    # only move if the orientation of the vehicle is horizontal
                    if neighbouring_veh.orientation == "H":
                        move_vehicle_ahead(neighbouring_veh, r, c)

                        # append move to DataFrame
                        append_move_to_DataFrame(neighbouring_veh, "right")

                        pick_free_square = False
                        break

                # move vehicle to the up respectively from free square
                elif r + 1 < grid_size \
                and occupation[r + 1][c] >= 1 and surr_square == "up":
                    neighbouring_veh = vehicle_dict[occupation[r + 1][c]]

                    # only move if the orientation of the vehicle is vertical
                    if neighbouring_veh.orientation == "V":
                        move_vehicle_back(neighbouring_veh, r, c)

                        # append move to DataFrame
                        append_move_to_DataFrame(neighbouring_veh, "up")

                        pick_free_square = False
                        break

                # move vehicle to the move respectively from free square
                elif r - 1 >= 0 and occupation[r - 1][c] >= 1 \
                and surr_square == "down":
                    neighbouring_veh = vehicle_dict[occupation[r - 1][c]]

                    # only move if the orientation of the vehicle is vertical
                    if neighbouring_veh.orientation == "V":
                        move_vehicle_ahead(neighbouring_veh, r, c)

                        # append move to DataFrame
                        append_move_to_DataFrame(neighbouring_veh, "down")

                        pick_free_square = False
                        break