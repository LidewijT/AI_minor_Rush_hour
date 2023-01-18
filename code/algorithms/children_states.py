import numpy as np
from ..classes import board


class State():
    def __init__(self, board, parent, state, layer_nbr):
        self.board = board
        # np array of parent state
        self.parent = parent
        # np array of current state
        self.state = state
        self.layer_nbr = layer_nbr

    def get_states(self):
            copied_current_sp = copy.deepcopy(board.occupation)
            states_list = [] # deze vullen met state classes

            for vehicle in self.vehicle_dict:

                movement_list = ["left", "right", "up", "down"]
                for movement_dir in movement_list:
                    # 'reset' occupation
                    self.board.occupation = copied_current_sp

                    if vehicle.orientation == "H":
                        # check if the tile to the left of the vehicle is occupied
                        if movement_dir == "left" and\
                        self.movement_check(0, vehicle, r=-1) == True:
                            # make movement
                            self.move_vehicle_back(vehicle, r=-1)

                            # append state to list
                            state_space_list.append(self.board.occupation)

                        # check if the tile to the right of the vehicle is occupied
                        elif movement_dir == "right" and\
                        self.movement_check(-1, vehicle, r=1) == True:
                            # make movement
                            self.move_vehicle_ahead(vehicle, vehicle, r=1)

                            # append state to list
                            state_space_list.append(self.board.occupation)

                    else:
                        # check if the tile above of the vehicle is occupied
                        if movement_dir == "up" and\
                        self.movement_check(0, vehicle, c=-1) == True:
                            # make movement
                            self.move_vehicle_back(vehicle, c=-1)

                            # append state to list
                            state_space_list.append(self.board.occupation)

                        # check if the tile below the vehicle is occupied
                        elif movement_dir == "down" and\
                        self.movement_check(-1, vehicle, c=1) == True:
                            # make movement
                            self.move_vehicle_ahead(vehicle, c=1)

                            # append state to list
                            state_space_list.append(self.board.occupation)

    def movement_check(self, direction, vehicle, r=0, c=0):
        """check if movement is possible"""
        # direction 0 for back, -1 for ahead
        veh_row, veh_column = vehicle.positions[direction]

        if self.board.occupation[(veh_row + r, veh_column + c)] == 0:
            return True

        else:
            return False

    def move_vehicle_back(self, vehicle, r=0, c=0):
        """
        Takes a vehicle object and updates its position based on the gives row
        and column. Updates the occupation matrix and the new vehicle positions.
        """
        veh_row, veh_column = vehicle.positions[0]

        # move vehicle backwards (left/up)
        vehicle.positions.insert(0, (veh_row + r, veh_column + c))
        self.board.occupation[vehicle.positions[-1]] = 0

        # update square the vehicle moved away from back to grey ("empty")
        self.empty_square(vehicle, -1)

        # update the positions the vehicle is at
        vehicle.positions = vehicle.positions[:-1]

    def move_vehicle_ahead(self, vehicle, r=0, c=0):
        veh_row, veh_column = vehicle.positions[-1]

        # move vehicle ahead (right/down)
        vehicle.positions.append((veh_row + r, veh_column + c))
        self.board.occupation[vehicle.positions[0]] = 0

        # update square the vehicle moved away from back to grey ("empty")
        self.empty_square(vehicle, 0)

        # update the positions the vehicle is at
        vehicle.positions = vehicle.positions[1:]
