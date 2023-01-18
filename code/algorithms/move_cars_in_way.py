from ..algorithms import randomise
import random
""""
Assumes that red car is horizontally oriented.
"""


def move_priority_red_car(test_board):
    # get information red car
    red_car = test_board.red_car
    # get square position of red car on exit site
    red_row, red_col = test_board.vehicle_dict[red_car].positions[-1]


    # check whether the red car is blocked
    if test_board.occupation[red_row, red_col + 1] == 0:
        # red car is not blocked, move it towards the exit
        test_board.move_vehicle_ahead(test_board.vehicle_dict[red_car], red_row, red_col + 1)

        return test_board.vehicle_dict[red_car], "right"

    # red car is blocked, so move the car that is blocking the exit
    else:
        # get the car that is in the way
        car_in_the_way = test_board.occupation[red_row, red_col + 1]
        car_move_pos = test_board.vehicle_dict[car_in_the_way].positions

        move_car(test_board, car_in_the_way, car_move_pos)

        # move car that is blocking the car that is in the way
        else:
            pass



def move_car(test_board, car, car_move_pos):
        # try to move the car
        if test_board.vehicle_dict[car].orientation == "H":
            # test move to left
            r, c = car_move_pos[0]
            if test_board.occupation[r, c - 1] == 0:
                # move left
                test_board.move_vehicle_back(test_board.vehicle_dict[car], r, c - 1)

            # test move to right
            r, c = car_move_pos[-1]
            if test_board.occupation[r, c + 1] == 0:
                # move right
                test_board.move_vehicle_ahead(test_board.vehicle_dict[car], r, c + 1)

        elif test_board.vehicle_dict[car].orientation == "V":
            # test move to up
            r, c = car_move_pos[0]

            if test_board.occupation[r - 1, c] == 0:
                # move up
                test_board.move_vehicle_back(test_board.vehicle_dict[car], r - 1, c)

            # test move to down
            r, c = car_move_pos[-1]
            if test_board.occupation[r + 1, c] == 0:
                # move down
                test_board.move_vehicle_ahead(test_board.vehicle_dict[car], r + 1, c)


