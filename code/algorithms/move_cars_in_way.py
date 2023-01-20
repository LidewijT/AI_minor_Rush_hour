from ..algorithms import randomise
import random
""""
Assumes that red car is horizontally oriented.
"""

def move_red_car(test_board):
    """
    Moves the red car if not blocked. Otherwise moves the car that is standing
    in the way.
    """
    # get red car number and its Vehicle object
    red_car_nr = test_board.red_car
    red_car = test_board.vehicle_dict[red_car_nr]

    # get square (row, column) of red car on exit site (es)
    red_r_es, red_c_es = red_car.positions[-1]

    # check whether the red car is blocked
    if test_board.occupation[red_r_es, red_c_es + 1] == 0:
        # do not move the red car forward if its last move was backwards         red car not blocked
        if red_car.movement != "back":
            # move it 1 step towards the exit                                    move red car
            test_board.move_vehicle_ahead(test_board.vehicle_dict[red_car_nr], red_r_es, red_c_es + 1)

            print("red car moved")
            return test_board.vehicle_dict[red_car_nr], "right"

        else:
            # change direction of red car back to None                           move car that was blocked by the red car
            red_car.movement = None

            # get car that was blocked by the red car
            blocked_veh, direction = red_car.blocking_veh
            red_car.blocking_veh = None

            # move the car that was blocked before to the free square
            car_movement(test_board, blocked_veh, direction, red_r_es, red_c_es + 1)


    # red car is blocked                                                         red car is blocked
    else:
        print("Red car blocked")
        # get the car number and object that is in the way
        car_in_the_way = test_board.occupation[red_r_es, red_c_es + 1]
        car_object = test_board.vehicle_dict[car_in_the_way]

        # try to move the car that is blocking the red car                       try to move car that is blocking the red car
        moved = move_blocking_vehicle(test_board, car_in_the_way, car_object)

        # check if a car was moved
        if moved[0] == True:                                                   # move car that was blocking the red car
            return moved[1], moved[2]

    # the vehicle that is blocking the red car is also being blocked
    veh_blocking = moved[1]
    veh_blocking_the_veh_block = []

    # move the vehicle(s) that is blocking this vehicle
    for veh in veh_blocking:
        moved = move_blocking_vehicle(test_board, veh, test_board.vehicle_dict[veh])

        if moved[0] == True:
            return moved[1], moved[2]

        else:
            veh_blocking_the_veh_block.append(moved[1])

    # move the vehicles that block the blocking vehicles
    print("move the vehicles that block the blocking vehicles")
    vb_vb_vb = []
    for vehs in veh_blocking_the_veh_block:
        for veh in vehs:
            the_move = move_blocking_vehicle(test_board, veh, test_board.vehicle_dict[veh])
            if the_move[0] == True:
                return the_move[1], the_move[2]

            else:
                vb_vb_vb.append(the_move[1])

    print("move vb vb vb")
    for vehs in vb_vb_vb:
        for veh in vehs:
            bla = move_blocking_vehicle(test_board, veh, test_board.vehicle_dict[veh])
            if bla[0] == True:
                return bla[1], bla[2]

            else:
                pass


    # set the direction to the opposite if it is assigned a direction
    for veh in veh_blocking:
        # get vehicle object
        veh_obj = test_board.vehicle_dict[veh]
        # change the direction if not None
        if veh_obj.movement == "back":
            veh_obj.movement = "ahead"

            print(f"changed direction of {veh} to ahead")

        elif veh_obj.movement == "ahead":
            veh_obj.movement = "back"
            print(f"changed direction of {veh} to back")

    print(f"\ntry to make a move again\n")
    move_red_car(test_board)




def move_blocking_vehicle(test_board, veh_nr, veh_object):
    print(f"Trying to move {veh_nr}")
    # get start and end of the car positions
    ahead_pos = veh_object.positions[-1]        # use for right/down
    back_pos = veh_object.positions[0]          # use for left/up

    # get all possible movements of the current vehicle based on its orientation
    if veh_object.orientation == "H":
        # left or right for horizontal orientation
        movements = {"back": [back_pos[0], back_pos[1] - 1, "left"], "ahead": [ahead_pos[0], ahead_pos[1] + 1, "right"]}

    else:
        # up or down for vertical orientation
        movements = {"back": [back_pos[0] - 1, back_pos[1], "up"], "ahead": [ahead_pos[0] + 1, ahead_pos[1], "down"]}

    # create list to keep track of possible vehicles blocking the current vehicle
    veh_blocking = []

    # loop over all possible ways to move the vehicle
    for direction, move in movements.items():

        # check if the move would be within the grid
        if 0 <= move[0] < test_board.grid_size and 0 <= move[1] < test_board.grid_size:

            # check if vehicle can move
            if test_board.occupation[move[0], move[1]] == 0 and \
                (veh_object.movement == None or veh_object.movement == direction):
                # move vehicle back (left or up)
                if direction == "back":
                    test_board.move_vehicle_back(veh_object, move[0], move[1])

                # move vehicle ahead (right or down)
                else:
                    test_board.move_vehicle_ahead(veh_object, move[0], move[1])

                # save the last move direction of vehicle
                veh_object.movement = direction

                return True, veh_object, move[2]

            else:
                if test_board.occupation[move[0], move[1]] != 0:
                    # get the vehicle that is blocking the way
                    veh_blocking.append(test_board.occupation[move[0], move[1]])

        else:
            # reset direction of the car if it is turned to move out of the grid
            veh_object.movement = None

    # return False if no vehicle could be moved and return the vehicles blocking this vehicle
    print(f"the blocked cars could not be moved: {veh_blocking}")

    return False, veh_blocking


def car_movement(test_board, vehicle, direction, r, c):
        # move vehicle to the left respectively from free square
        if direction == "left":
            test_board.move_vehicle_back(vehicle, r, c)

        # move vehicle to the right respectively from free square
        elif direction == "right":
            test_board.move_vehicle_ahead(vehicle, r, c)

        # move vehicle to the up respectively from free square
        elif direction == "up":
            test_board.move_vehicle_back(vehicle, r, c)

        # move vehicle to the move respectively from free square
        elif direction == "down":
            test_board.move_vehicle_ahead(vehicle, r, c)








        # if test_board.vehicle_dict[car].orientation == "H":
        #     # test move to left
        #     r, c = car_move_pos[0]
        #     if test_board.occupation[r, c - 1] == 0:
        #         # move left
        #         test_board.move_vehicle_back(test_board.vehicle_dict[car], r, c - 1)

        #     # test move to right
        #     r, c = car_move_pos[-1]
        #     if test_board.occupation[r, c + 1] == 0:
        #         # move right
        #         test_board.move_vehicle_ahead(test_board.vehicle_dict[car], r, c + 1)

        # elif test_board.vehicle_dict[car].orientation == "V":
        #     # test move to up
        #     r, c = car_move_pos[0]

        #     if test_board.occupation[r - 1, c] == 0:
        #         # move up
        #         test_board.move_vehicle_back(test_board.vehicle_dict[car], r - 1, c)

        #     # test move to down
        #     r, c = car_move_pos[-1]
        #     if test_board.occupation[r + 1, c] == 0:
        #         # move down
        #         test_board.move_vehicle_ahead(test_board.vehicle_dict[car], r + 1, c)


