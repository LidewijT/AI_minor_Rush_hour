"""
Picks one random car movement of the given board and returns this movement.
"""

import random
import numpy as np

def random_car_move(test_board, move_again=False):
    """
    Picks a random vehicle to move.
    """
    # get all free squares
    free_row, free_col = test_board.get_free_squares()
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

            # make movement with the given surr_square
            vehicle, new_r, new_c = test_board.car_move(surr_square, r, c)

            if vehicle:
                veh_list = [(vehicle, surr_square)]

                while move_again == True or random.random() < 0.01:
                    vehicle, new_r, new_c = test_board.car_move(surr_square, new_r, new_c)
                    veh_list.append(vehicle, surr_square)

                return veh_list

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
