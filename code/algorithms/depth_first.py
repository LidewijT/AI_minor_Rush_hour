import pandas as pd
import copy

from itertools import chain
from ..classes.board import Board

class Depth_First_Search():
    """
    This class computes the depth-first search algorithm, which travers in a
    tree data structure based on a dictionary. The algorithm explores as fas as
    possible along each branch before backtracking. This exploration does not go
    deeper when it reached a winning state, then it will start backtracking the
    moves into a dataframe.
    """

    def __init__(self, start_state, max_depth=None):
        """
        Initializes the class by setting the start state, exit tile, red car
        name, and runs the algorithm. Afterwards, it puts all moves of the
        solution ordered into a dataframe.
        """
        # attributes
        self.board = start_state
        self.start_state = copy.copy(start_state.board)
        self.exit_tile = start_state.exit_tile
        self.red_car = start_state.red_car
        self.max_depth = max_depth
        self.won = False

        # create dictionary to keep track of all states. Key values are children
        # and the corresponding value is a tuple of (move, parent)
        self.children_parent_dict = {
            hash(tuple(chain.from_iterable(self.start_state))):
            (None, None, 0)
        }

        # run the algorithm
        self.run()

        # moves to dataframe
        if self.won == True:
            self.moves_to_df(self.current_state)

    def run(self):
        """
        Starts running the algorithm until the board is in a winning position:
        the red car is at the exit tile.
        """
        # initialize the stack with the starting state
        self.stack = [self.start_state]

        while self.stack != []:
            # get next state
            self.current_state = self.get_next_state()

            # get all the children states of the current state
            self.won = self.build_children()

            # stop if a solution was created
            if self.won == True:
                return

    def get_next_state(self):
        """
        Returns the last element of de stack while removing it at the same time.
        """
        return self.stack.pop()

    def build_children(self):
        """
        Get all the children of the input state and add them the dictionary.
        Creation of children are done by moving one car, checked for their
        uniqueness, and adds them to the stack. Also checks if red car
        is at winning position.
        """
        # save parent state
        parent_state = copy.copy(self.current_state)

        # convert nparray to hashed flattened tuple for dictionary
        parent_occupation_hash = hash(tuple(chain.from_iterable(parent_state)))

        # get lists for free squares and their surrounding directions
        free_row, free_col = Board.get_free_squares(
            self.board,
            self.current_state
        )
        direction_list = ["left", "right", "up", "down"]

        # systematically go through the free squares to create children
        for free_tile_nr in range(len(free_row)):
            r, c = free_row[free_tile_nr], free_col[free_tile_nr]

            # systematically go through all sides of the free square
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

                    # check if state is unique
                    if current_occupation_hash not in self.children_parent_dict:

                        # save child in dictionary with (move, parent)
                        self.children_parent_dict[current_occupation_hash] = \
                            ((vehicle.car, direction), parent_occupation_hash)

                        # solution if the red car is at the exit
                        if self.current_state[self.exit_tile] == self.red_car:
                            return True

                        # add child to list
                        self.stack.append(self.current_state)

                    # reset the current state as parent state for next child
                    self.current_state = copy.copy(parent_state)


    def append_move_to_DataFrame_reversed(self, moves_df, move):
        """
        Appends the input move to the existing dataframe, saving the car name
        and the corresponding move.
        """
        # append move to DataFrame in reverse order since you start at the
        # winning state
        move_df = pd.DataFrame(
            [[move[0], move[1]]],
            columns=['car name', 'move']
        )

        return pd.concat([move_df, moves_df])

    def moves_to_df(self, child):
        """
        Creates an empty dataframe for the moves of the optimal solution found.
        Searches back in the children_parent_dict using the input child to find
        all moves made to get the winning state.
        """
        # create empty dataframe
        self.moves_df = pd.DataFrame(columns=['car name', 'move'])

        # create key to search back in dictionary
        child_hash = hash(tuple(chain.from_iterable(child)))

        # search back in dict to find all the moves made to get to winning state
        while self.children_parent_dict[child_hash][0] != None:
            values = self.children_parent_dict[child_hash]

            # put move into df
            self.moves_df = self.append_move_to_DataFrame_reversed(
                self.moves_df,
                values[0]
            )

            # parent is the child for next move
            child_hash = values[1]
