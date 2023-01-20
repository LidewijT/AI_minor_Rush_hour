from ..algorithms import randomise
from ..algorithms import breath_first

import random
""""
Assumes that red car is horizontally oriented.
"""


def move_priority_red_car(test_board):
    # get information red car
    red_car = test_board.red_car
    # get square position of red car on exit site
    red_row, red_col = test_board.vehicle_dict[red_car].positions[-1]


    # move red car if not blocked with a 75% chance
    if test_board.occupation[red_row, red_col + 1] == 0 and random.random() > 0.4:
        # red car is not blocked, move it towards the exit
        test_board.move_vehicle_ahead(test_board.vehicle_dict[red_car], red_row, red_col + 1)

        return test_board.vehicle_dict[red_car], "right"

    else:
        # red car is blocked, so move random car
        return breath_first.breath_first_search(test_board)







# def move_cars(self):
#         copied_current_sp = copy.deepcopy(self.occupation)
#         state_space_list = []

#         for vehicle in self.vehicle_dict:

#             movement_list = ["left", "right", "up", "down"]
#             for movement_dir in movement_list:
#                 # 'reset' occupation
#                 self.occupation = copied_current_sp

#                 if vehicle.orientation == "H":
#                     # check if the tile to the left of the vehicle is occupied
#                     if movement_dir == "left" and\
#                     self.movement_check(0, vehicle, r=-1) == True:
#                         # make movement
#                         self.move_vehicle_back(vehicle, r=-1)

#                         # append state to list
#                         state_space_list.append(self.occupation)

#                     # check if the tile to the right of the vehicle is occupied
#                     elif movement_dir == "right" and\
#                     self.movement_check(-1, vehicle, r=1) == True:
#                         # make movement
#                         self.move_vehicle_ahead(vehicle, vehicle, r=1)

#                         # append state to list
#                         state_space_list.append(self.occupation)

#                 else:
#                     # check if the tile above of the vehicle is occupied
#                     if movement_dir == "up" and\
#                     self.movement_check(0, vehicle, c=-1) == True:
#                         # make movement
#                         self.move_vehicle_back(vehicle, c=-1)

#                         # append state to list
#                         state_space_list.append(self.occupation)

#                     # check if the tile below the vehicle is occupied
#                     elif movement_dir == "down" and\
#                     self.movement_check(-1, vehicle, c=1) == True:
#                         # make movement
#                         self.move_vehicle_ahead(vehicle, c=1)

#                         # append state to list
#                         state_space_list.append(self.occupation)

#     def movement_check(self, direction, vehicle, r=0, c=0):
#         """check if movement is possible"""
#         # direction 0 for back, -1 for ahead
#         veh_row, veh_column = vehicle.positions[direction]

#         if self.occupation[(veh_row + r, veh_column + c)] == 0:
#             return True

#         else:
#             return False

#     def move_vehicle_back(self, vehicle, r=0, c=0):
#         """
#         Takes a vehicle object and updates its position based on the gives row
#         and column. Updates the occupation matrix and the new vehicle positions.
#         """
#         veh_row, veh_column = vehicle.positions[0]

#         # move vehicle backwards (left/up)
#         vehicle.positions.insert(0, (veh_row + r, veh_column + c))
#         self.occupation[vehicle.positions[-1]] = 0

#         # update square the vehicle moved away from back to grey ("empty")
#         self.empty_square(vehicle, -1)

#         # update the positions the vehicle is at
#         vehicle.positions = vehicle.positions[:-1]

#     def move_vehicle_ahead(self, vehicle, r=0, c=0):
#         veh_row, veh_column = vehicle.positions[-1]

#         # move vehicle ahead (right/down)
#         vehicle.positions.append((veh_row + r, veh_column + c))
#         self.occupation[vehicle.positions[0]] = 0

#         # update square the vehicle moved away from back to grey ("empty")
#         self.empty_square(vehicle, 0)

#         # update the positions the vehicle is at
#         vehicle.positions = vehicle.positions[1:]
