from ..classes import game
from ..classes import board

import numpy as np
import pandas as pd
import queue
import copy


class Breath_first_search():
    def __init__(self, start_state):
        self.start_state = start_state
        self.moves_df = pd.DataFrame(columns=['car name', 'move'])

        # save variables locally to improve runtime
        self.exit_tile = start_state.exit_tile
        self.red_car = start_state.red_car

        # start the algorithm
        self.breath_first_search()

        print(f"number of visited states: {len(self.children_parent_dict)}")

        # string the moves leading up to the winning state together
        self.string_moves_together()

    def breath_first_search(self):
        """
        Goes trough a breath first search algorithm until a winning state is reached
        """
        # dictionary with children as key and as value a tuple of (move, parent)
        # where move is also a tuple of (vehicle, direction)
        self.children_parent_dict = \
        {tuple([tuple(row) for row in self.start_state.occupation]): None}

        # start a queue
        self.q = queue.Queue()
        self.q.put(self.start_state)

        while not self.q.empty():
            current_state = self.q.get()

            # get list of possible children current state can give
            won = self.get_next_states(current_state)

            if won == "yes":
                return

    def get_next_states(self, current_state):
        """
        gets all the possible children states the current state can give
        adds this to a list
        """
        next_states = []

        # save the parent state to recall back to
        parent_state = copy.deepcopy(current_state)

        # save the parent occupation as a tuple so it is hashable
        parent_occupation_tuple = \
        tuple([tuple(row) for row in parent_state.occupation])

        # retrieve lists of the free rows and columns
        free_row, free_col = parent_state.get_free_squares()
        direction_list = ["left", "right", "up", "down"]

        # systimatically go trough the empty tiles
        for free_tile_nbr in range(len(free_row)):
            r, c = free_row[free_tile_nbr], free_col[free_tile_nbr]

            for direction in direction_list:
                # if possible move car to given direction (else it returns None)
                vehicle = current_state.car_move(direction, r, c)

                # if a valid move was made
                if vehicle:
                    # convert occupation to tuple of tuples to make it hashable
                    child_occupation_tuple = \
                    tuple([tuple(row) for row in current_state.occupation])

                    # check if this state is unique (pruning)
                    if child_occupation_tuple not in self.children_parent_dict:
                        # put child in queue
                        self.q.put(current_state)

                        # add child occupation tuple to children parent dict
                        self.children_parent_dict[child_occupation_tuple] = \
                        (vehicle.car, direction), parent_occupation_tuple

                        # check if this is a winning board
                        if current_state.occupation[self.exit_tile] == self.red_car:
                            self.child_tuple = child_occupation_tuple
                            return "yes"

                    # reset state
                    current_state = copy.deepcopy(parent_state)

        return next_states

    def string_moves_together(self):
        """
        Search back in child parent dictionary to find all
        the moves made to get to winning state
        """
        while self.children_parent_dict[self.child_tuple] != None:
            move, parent = self.children_parent_dict[self.child_tuple]
            self.child_tuple = parent

            self.append_move_to_DataFrame_reversed(move)

    def append_move_to_DataFrame_reversed(self, move):
        """
        Append move to DataFrame in reverse order since you start at the end state
        """
        move_df = pd.DataFrame([[move[0], move[1]]], columns=['car name', 'move'])
        self.moves_df = pd.concat([move_df, self.moves_df])
