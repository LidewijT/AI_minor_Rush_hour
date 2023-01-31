"""
Picks one random car movement of the given board and returns this movement.
"""

import random
import numpy as np
from ..classes.board import Board

def random_car_move(test_board, occupation_board, _):
    """
    Picks a random vehicle to move.
    """
    # get all free squares
    free_row, free_col = Board.get_free_squares(test_board, occupation_board)
    # pick random free square until vehicle moves
    pick_free_square = True

    while pick_free_square == True:
        # get the position of a randomly chosen free square
        free_row, free_col, r, c = random_free_square(free_row, free_col)

        # load_vehicles
        # list for random squares around free square
        surrounding_squares = ["left", "right", "up", "down"]

        # pick until all surroundings squares have been tried
        for _ in range(len(surrounding_squares)):
            # choose a random surrounding square
            surr_square, surrounding_squares = random_surrounding_square(surrounding_squares)

            # make movement with the given surr_square
            vehicle, occupation_board = Board.car_move(test_board, occupation_board, surr_square, r, c)

            # return if a vehicle was found to move and the updated board
            if vehicle:
                return occupation_board, vehicle, surr_square

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
