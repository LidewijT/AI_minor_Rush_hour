from ..classes import game
from ..classes import board

import queue
import copy


def breath_first_search(start_state):
    moves_df = pd.DataFrame(columns=['car name', 'move'])
    child, children_parent_dict = search(start_state)
    print("test")
    # search back in dict to find all the moves made to get to winning state
    while children_parent_dict[child] != None:
        move, parent = children_parent_dict[child]
        child = parent

        # put move into df
        moves_df = append_move_to_DataFrame_reversed(moves_df, move)

    return moves_df


def search(start_state):
    # dictionary with children as key and as value a tuple of (move, parent)
    # where move is also a tuple of (vehicle, direction)
    children_parent_dict = {start_state: None}

    visited = set()
    q = queue.Queue()
    q.put(start_state)

    while not q.empty():
        current_state = q.get()
        print(current_state.test_board.occupation)

        if current_state.test_board.occupation[current_state.test_board.exit_tile] \
        == current_state.test_board.red_car:
        # game.Game.win_check(current_state) == True:
            return current_state, children_parent_dict

        if current_state in visited:
            continue

        visited.add(current_state)

        for next_state in get_next_states(current_state):
            q.put(next_state)

    return None



def get_next_states(current_state):
    next_states = []

    parent_state = copy.deepcopy(current_state)

    free_row, free_col = current_state.get_free_squares()

    direction_list = ["left", "right", "up", "down"]

    # systimatically go trough the empty tiles
    for free_tile_nbr in range(free_row):

        r, c = free_row[free_tile_nbr], free_col[free_tile_nbr]

        for direction in direction_list:
            # make movement with the given surr_square
            vehicle = current_state.car_move(direction, r, c)

            if vehicle:
                next_states.append(current_state)
                children_parent_dict[current_state.occupation] = ((vehicle.car, direction), parent_state.occupation)

                # "reset" curent state
                current_state = copy.deepcopy(parent_state)



def append_move_to_DataFrame_reversed(moves_df, move):
    # append move to DataFrame in reverse order since you start at the end
    move_df = pd.DataFrame([[move[0], move[1]]], columns=['car name', 'move'])
    moves_df = pd.concat([moves_df, move_df])
