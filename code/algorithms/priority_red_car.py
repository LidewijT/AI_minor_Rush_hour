from ..algorithms import randomise
from ..algorithms import breath_first

import random
""""
Assumes that red car is horizontally oriented.
"""

def move_priority_red_car(test_board, occupation_board, percentage):
    # get information red car
    red_car = test_board.red_car
    # get exit site
    exit_row = test_board.exit_tile[0]

    # get square position of red car on exit site
    # red_row, red_col = test_board.vehicle_dict[red_car].positions[-1]
    for col in range(test_board.exit_tile[1]):
        if occupation_board[exit_row][col] == red_car:
            red_car_position = (exit_row, col)

    # move red car to the exit (right) if not blocked with a given chance
    if occupation_board[red_car_position[0], red_car_position[1] + 1] == 0 and random.random() <= percentage:
        # red car is not blocked, move it towards the exit
        vehicle_obj, occupation_board = test_board.car_move(occupation_board, "right", red_car_position[0], red_car_position[1] + 1)

        return occupation_board, vehicle_obj, "right"

    else:
        # red car is blocked, so move random car
        return randomise.random_car_move(test_board, occupation_board, None)
