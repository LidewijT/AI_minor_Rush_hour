from ..classes import game
from ..classes import board

import numpy as np
import pandas as pd
import queue
import copy


def breath_first_search(start_state):
    # initiate a dataframe to append the made moves to
    moves_df = pd.DataFrame(columns=['car name', 'move'])

    # search breath first
    child, children_parent_dict = search(start_state)
    child_tuple = tuple([tuple(row) for row in child.occupation])

    print(f"number: {len(children_parent_dict)}")

    # search back in dict to find all the moves made to get to winning state
    while children_parent_dict[child_tuple] != None:
        move, parent = children_parent_dict[child_tuple]
        # print(parent)
        child_tuple = parent

        moves_df = append_move_to_DataFrame_reversed(moves_df, move)

    return moves_df


def search(start_state):
    # dictionary with children as key and as value a tuple of (move, parent)
    # where move is also a tuple of (vehicle, direction)
    children_parent_dict = {tuple([tuple(row) for row in \
    start_state.occupation]): None}

    q = queue.Queue()
    q.put(start_state)

    while not q.empty():
        current_state = q.get()

        # check if winning condtion is reached
        if current_state.occupation[current_state.exit_tile] \
        == current_state.red_car:
            return current_state, children_parent_dict

        # get list of possible children current state can give
        next_states_list, children_parent_dict = \
        get_next_states(current_state, children_parent_dict)

        # put these children states in the queue
        for next_state in next_states_list:
            q.put(next_state)


def get_next_states(current_state, children_parent_dict):
    next_states = []

    # save the parent state to recall back to
    parent_state = copy.deepcopy(current_state)

    # safe the parent occupation as a tuple so it is hashable
    parent_occupation_tuple = tuple([tuple(row) for row in \
    parent_state.occupation])

    # retrieve lists of the free rows and columns
    free_row, free_col = parent_state.get_free_squares()

    direction_list = ["left", "right", "up", "down"]

    # systimatically go trough the empty tiles
    for free_tile_nbr in range(len(free_row)):

        r, c = free_row[free_tile_nbr], free_col[free_tile_nbr]

        for direction in direction_list:
            # make movement with the given direction, returns None if invalid move
            vehicle = current_state.car_move(direction, r, c)

            if vehicle:
                # convert occupation to tuple of tuples to make it hashable
                child_occupation_tuple = tuple([tuple(row) for row in \
                current_state.occupation])

                # check if this state is unique (pruning)
                if child_occupation_tuple not in children_parent_dict:
                    # append child to next states list and children parent dict
                    next_states.append(current_state)

                    children_parent_dict[child_occupation_tuple] = \
                    ((vehicle.car, direction), parent_occupation_tuple)

                # reset state
                current_state = copy.deepcopy(parent_state)

    return next_states, children_parent_dict


def append_move_to_DataFrame_reversed(moves_df, move):
    # append move to DataFrame in reverse order since you start at the end
    move_df = pd.DataFrame([[move[0], move[1]]], columns=['car name', 'move'])
    moves_df = pd.concat([move_df, moves_df])

    return moves_df
