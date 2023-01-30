from .depth_first import DepthFirst
from itertools import chain
import copy

class PriorityChildren(DepthFirst):
    """
    This subclass of DepthFirst provides an implementation of the A* search
    algorithm. It has the ability to prioritize the order in which the children
    states are added to the stack by assigning each state a priority value. This
    is based on the number of blocking vehicles beween the red car and the exit
    and based on the number of squares the red car is away from the exit. It
    ensures that the most promising child is exploren first.
    """

    def build_children(self, depth):
        """
        Get all the children of the input state and add them the dictionary.
        Creation of children are done by moving one car, checked for their
        uniqueness and depth, and adds them to the stack in a prioritized order.
        Also checks if red car is at winning position.
        """
        children_list = []

        # save parent state
        parent_state = copy.deepcopy(self.current_state)

        parent_occupation_hash = hash(tuple(chain.from_iterable(parent_state.occupation)))

        # get lists for free squares and their surrounding directions
        free_row, free_col = self.current_state.get_free_squares()
        direction_list = ["left", "right", "up", "down"]

        # systematically go through the free squares to create children
        for free_tile_nbr in range(len(free_row)):

            r, c = free_row[free_tile_nbr], free_col[free_tile_nbr]

            # systematically go through all sides of the empty square
            for direction in direction_list:
                # make movement with the given surrounding square
                vehicle = self.current_state.car_move(direction, r, c)

                # check if a vehicle was found on the surrounding square
                if vehicle:
                    # convert nparray to hashed flattened tuple
                    current_occupation_hash = hash(tuple(chain.from_iterable( \
                        self.current_state.occupation)))

                    # check if state is unique or is better (lower depth)
                    if current_occupation_hash not in self.children_parent_dict\
                        or self.children_parent_dict[current_occupation_hash] \
                            [2] > depth:

                        # save child in dictionary with (move, parent, depth)
                        self.children_parent_dict[current_occupation_hash] = \
                            ((vehicle.car, direction), parent_occupation_hash, \
                                 depth)

                        # solution if the red car is at the exit
                        if self.current_state.occupation[self.exit_tile] == \
                            self.red_car:
                            return True

                        # get the priority value of the current child
                        self.check_blocking_cars(self.current_state)
                        children_list.append(self.current_state)

                    # reset the current state as parent state for next child
                    self.current_state = copy.deepcopy(parent_state)

        # sort by heuristic
        self.sort_children_states(children_list, depth)

    def sort_children_states(self, children_states, depth):

        # descending order
        sorted_children_states = sorted(children_states, reverse=True)
        for child in sorted_children_states:
            self.stack.append((child, depth))

    def check_blocking_cars(self, state):
        """
        Calculates priority value based on blocking cars before exit for red car
        """
        # get red car position of exit site of state:
        red_car_position = state.vehicle_dict[self.red_car].positions[-1]
        blocking_cars = 0
        squares_to_exit = 0

        # go through every column
        for c in range(self.exit_tile[1] - red_car_position[1]):
            # get the value of the square to check if there is a vehicle
            if state.occupation[red_car_position[0]][red_car_position[1] + \
                c+1] > 0:
                blocking_cars += 1
            squares_to_exit += 1

        state.priority = blocking_cars
        state.squares_to_exit = squares_to_exit

        return blocking_cars

