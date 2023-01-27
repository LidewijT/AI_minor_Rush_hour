from ..algorithms import randomise
import random
from itertools import chain
""""
Assumes that red car is horizontally oriented.
"""

class Move_blocking_cars():
    def __init__(self, test_board):
        self.test_board = test_board
        self.red_car_nr = test_board.red_car
        self.red_car = test_board.vehicle_dict[self.red_car_nr]

    def move_red_car(self):
        """
        Moves the red car if not blocked. Otherwise moves the car that is standing
        in the way.
        """

        # get square (row, column) of red car on exit site (es)
        self.red_r_es, self.red_c_es = self.red_car.positions[-1]

        # check whether the red car is blocked                                   red car not blocked
        if self.test_board.occupation[self.red_r_es, self.red_c_es + 1] == 0:
            # do not move the red car forward if its last move was backwards
            if self.red_car.movement != "back":                                # move red car
                # move it 1 step towards the exit
                self.test_board.move_vehicle_ahead(self.red_car, self.red_r_es, self.red_c_es + 1)

                self.red_car.blocked_by = []
                print("red car moved")
                return self.test_board.vehicle_dict[self.red_car_nr], "right"

            else:                                                              # move car that was blocked by the red car
                # reset movement of the red car
                self.red_car.movement = None
                # get car that was blocked by the red car
                blocked_veh, direction = self.red_car.blocking_veh
                self.red_car.blocking_veh = None

                # move the car that was blocked before to the free square
                if direction == "ahead":
                    self.test_board.move_vehicle_ahead(blocked_veh, self.red_r_es, self.red_c_es + 1)
                else:
                    self.test_board.move_vehicle_back(blocked_veh, self.red_r_es, self.red_c_es + 1)

        # red car is blocked
        else:                                                                  # red car is blocked
            print("Red car blocked")
            # get the car number and object that is in the way
            car_in_the_way = self.test_board.occupation[self.red_r_es, self.red_c_es + 1]
            car_object = self.test_board.vehicle_dict[car_in_the_way]

            # try to move the car that is blocking the red car                   try to move car that is blocking the red car
            moved = self.try_move_vehicle(car_in_the_way, car_object)

            # check if a car was moved
            if moved == True:                                                  # move car that was blocking the red car
                return self.moved_veh, self.move

            else:
                # update that the red car is blocked by this vehicle
                self.red_car.blocked_by.append(car_in_the_way)

                # move ..
                self.move_block_chain(car_object)


    def try_move_vehicle(self, veh_nr, veh_object):
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

        # loop over all possible ways to move the vehicle
        for direction, move in movements.items():

            # check if the move would be within the grid
            if 0 <= move[0] < self.test_board.grid_size and 0 <= move[1] < self.test_board.grid_size:

                # check if vehicle can move
                if self.test_board.occupation[move[0], move[1]] == 0 and \
                    (veh_object.movement == None or veh_object.movement == direction):
                    # move vehicle back (left or up)
                    if direction == "back":
                        self.test_board.move_vehicle_back(veh_object, move[0], move[1])
                    # move vehicle ahead (right or down)
                    else:
                        self.test_board.move_vehicle_ahead(veh_object, move[0], move[1])

                    # save the last move direction of vehicle
                    veh_object.movement = direction
                    veh_object.blocked_by = []
                    print(veh_nr, veh_object.blocked_by)

                    self.move = move[2]
                    self.moved_veh = veh_object

                    return True

                elif self.test_board.occupation[move[0], move[1]] == self.red_car_nr:
                    self.red_car.blocking_veh = veh_object, direction
                    


                    # save the vehicle that is blocking the way if it is not already in the list
                    if veh_object.blocked_by.count(self.test_board.occupation[move[0], move[1]]) == 0:
                        veh_object.blocked_by.append(self.test_board.occupation[move[0], move[1]])
                        pass

                else:
                    square_occupation = self.test_board.occupation[move[0], move[1]]

                    # save the vehicle that is blocking the way if it is not already in the list
                    if square_occupation != 0 and veh_object.blocked_by.count(square_occupation) == 0:
                        veh_object.blocked_by.append(self.test_board.occupation[move[0], move[1]])

            else:
                # reset direction of the car if it is turned to move out of the grid
                veh_object.movement = None


        # return False if no vehicle could be moved and return the vehicles blocking this vehicle
        print(f"the blocked cars could not be moved: {veh_object.blocked_by}")

        return False


    def car_movement(self, vehicle, direction, r, c):
            # move vehicle to the left respectively from free square
            if direction == "left":
                self.move_vehicle_back(vehicle, r, c)

            # move vehicle to the right respectively from free square
            elif direction == "right":
                self.move_vehicle_ahead(vehicle, r, c)

            # move vehicle to the up respectively from free square
            elif direction == "up":
                self.move_vehicle_back(vehicle, r, c)

            # move vehicle to the move respectively from free square
            elif direction == "down":
                self.move_vehicle_ahead(vehicle, r, c)

    def move_block_chain(self, veh_object):
        """
        The vehicle blocking the red car is blocked. Move all vehicles necessary
        to move this vehicle. Returns all moves.
        """

        result = veh_object.blocked_by

        # look 6 cars further
        for _ in range(6):
            # try to move these vehicles (layer n)
            result = self.move_blocking_vehicle(result)

            if result == True:
                return self.moved_veh, self.move

            # unnest list
            result = list(chain.from_iterable(result))

        # change direction and repeat
        for veh in veh_object.blocked_by:
            # get vehicle object
            veh_obj = self.test_board.vehicle_dict[veh]
            # change the direction if not None
            if veh_obj.movement == "back":
                veh_obj.movement = "ahead"

                print(f"changed direction of {veh} to ahead")

            elif veh_obj.movement == "ahead":
                veh_obj.movement = "back"
                print(f"changed direction of {veh} to back")

        print(f"\ntry to make a move again\n")

        # look 6 cars further
        for _ in range(6):
            # try to move these vehicles (layer n)
            result = self.move_blocking_vehicle(result)

            if result == True:
                return self.moved_veh, self.move

            # unnest list
            result = list(chain.from_iterable(result))

        print("did not work")

    def move_blocking_vehicle(self, veh_blocking):
        blocking_veh = []
        for veh in veh_blocking:
            moved = self.try_move_vehicle(veh, self.test_board.vehicle_dict[veh])

            # stop
            if moved == True:
                return moved

            blocking_veh.append(self.test_board.vehicle_dict[veh].blocked_by)

        return blocking_veh