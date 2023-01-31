from .depth_first import Depth_First_Search
from ..classes.board import Board
import copy
from itertools import chain
import pandas as pd

class Depth_Limited_Search(Depth_First_Search):
    """
    This class is a subclass of the Depth_First_Search and performs a depth-
    first search algorithm with a limited depth, set in the init method, which
    also runs the algorithm. The run method creates new children states if the
    maximum depth is not reached and until the board is in a winnig position.
    """

    def run(self, start_depth=0):
        """
        Has an initialized starting depth of 0, which is the initial state of
        the board. Each new child generation is depth + 1. Starts running the
        depth limited search algorithm and makes children states, if the max
        depth is not exceeded, until the board is in a winning position: the red
        car is at the exit tile.
        """
        # initialize the stack with the starting state and the starting depth
        self.stack = [(self.start_state, start_depth)]

        while self.stack != []:
            # get next state
            self.current_state, depth = self.get_next_state()

            # go to next state if we are deeper than current minimal solution
            if depth >= self.max_depth:
                continue

            # get all the children states of the current state
            self.won = self.build_children(depth + 1)

            # stop if a solution was created
            if self.won == True:
                return

        self.won = False

    def build_children(self, depth):
        """
        Get all the children of the input state and add them the dictionary.
        Creation of children are done by moving one car, checked for their
        uniqueness and depth, and adds them to the stack. Also checks if red car
        is at winning position.
        """
        # save parent state
        parent_state = copy.copy(self.current_state)

        # parent_occupation_hash = hash(parent_state)
        parent_occupation_hash = hash(tuple(chain.from_iterable(parent_state)))


        # get lists for free squares and their surrounding directions
        free_row, free_col = Board.get_free_squares(
            self.board,
            self.current_state
        )
        direction_list = ["left", "right", "up", "down"]

        # systematically go through the free squares to create children
        for free_tile_nbr in range(len(free_row)):

            r, c = free_row[free_tile_nbr], free_col[free_tile_nbr]

            # systematically go through all sides of the empty square
            for direction in direction_list:
                # make movement with the given surrounding square
                vehicle, self.current_state = Board.car_move(
                    self.board,
                    self.current_state,
                    direction,
                    r,
                    c
                )

                # check if a vehicle was found on the surrounding square
                if vehicle != False:
                    # convert nparray to hashed flattened tuple
                    current_occupation_hash = hash(tuple(
                        chain.from_iterable(self.current_state))
                    )

                    # check if state is unique or is better (lower depth)
                    if current_occupation_hash not in self.children_parent_dict\
                        or self.children_parent_dict[current_occupation_hash] \
                            [2] > depth:

                        # save child in dictionary with (move, parent, depth)
                        self.children_parent_dict[current_occupation_hash] = (
                            (vehicle.car, direction),
                            parent_occupation_hash,
                            depth
                        )

                        # solution if the red car is at the exit
                        if self.current_state[self.exit_tile] == self.red_car:
                            return True

                        # add child to list
                        self.stack.append((self.current_state, depth))

                    # reset the current state as parent state for next child
                    self.current_state = copy.copy(parent_state)
