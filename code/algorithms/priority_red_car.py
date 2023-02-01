import random

from ..algorithms import randomise

""""
Assumes that red car is horizontally oriented.
"""

def move_priority_red_car(test_board, occupation_board, percentage):
    """
    This function is a heuristic of the randomise algorithm. First, it finds the
    red car and the exit tile position on the board. Then it checks if the red
    car is blocked from moving to the exit (to the right) and, with a given
    chance (determined by the "percentage" parameter), moves the red car one
    square towards the exit (assuming its horizontally orientated). If the red
    car is blocked, the function calls another function "random_car_move" to
    move a random car. The function returns the updated occupation board, the
    moved vehicle object and the direction of movement.
    """
    # get information red car
    red_car = test_board.red_car
    # get exit site
    exit_row = test_board.exit_tile[0]

    # get square position of red car on exit site
    for col in range(test_board.exit_tile[1]):
        if occupation_board[exit_row][col] == red_car:
            red_car_position = (exit_row, col)

    # move red car to the exit (right) if not blocked with a given chance
    if occupation_board[red_car_position[0], red_car_position[1] + 1] == 0 \
        and random.random() <= percentage:
        # red car is not blocked, move it towards the exit
        vehicle_obj, occupation_board = test_board.car_move(
            occupation_board,
            "right",
            red_car_position[0],
            red_car_position[1] + 1
        )

        return occupation_board, vehicle_obj, "right"

    else:
        # red car is blocked, so move random car
        return randomise.random_car_move(test_board, occupation_board, None)
