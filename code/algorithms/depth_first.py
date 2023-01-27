import pandas as pd
import copy
import time
from itertools import chain

class DepthFirst():
    """
    This class computes the depth-first search algorithm, which travers in a
    tree data structure based on a dictionary. The algorithm explores as fas as
    possible along each branch before backtracking. This exploration does not go
    deeper when it reached the maximum depth or a winning state, then it will
    start backtracking.
    """
    def __init__(self, start_state):
        """
        Initializes the class by setting the start state, exit tile, red car
        name, and maximum depth, and runs the algorithm. Afterwards, it puts all
        moves of the optimal solution ordered into a dataframe.
        """
        # keep track of time
        start_time = time.time()

        # attributes
        self.start_state = start_state
        self.exit_tile = start_state.exit_tile
        self.red_car = self.start_state.red_car

        # set maximum depth the algorithm can go
        self.max_depth = 1000

        # create dictionary to keep track of all states. Key values are children
        # and the corresponding value is a tuple of (move, parent, depth)
        self.children_parent_dict = {hash(tuple(chain.from_iterable(start_state.occupation))): (None, None, 0)}

        # run the algorithm
        self.run()

        # moves to dataframe
        print("Export moves to dataframe...")
        self.moves_to_df(self.current_state)

        print(f"Time to get a solution {time.time() - start_time}")
        print(f"number states: {len(self.children_parent_dict)}")
        print(f"number moves: {len(self.moves_df)}")

    def run(self):
        """
        Starts running the algorithm until the board is in a winning position:
        the red car is at the exit tile.
        """
        # initialize start depth of the algorithm
        start_depth = 0
        # initialize the stack with the starting state and the starting depth
        self.stack = [(self.start_state, start_depth)]

        while self.stack != []:
            # get next state
            self.current_state, depth = self.get_next_state()

            # go to next state if we are deeper than current minimal solution
            if depth >= self.max_depth:
                continue

            # get all the children states of the current state
            won = self.build_children(depth + 1)

            # stop if a solution was created
            if won == True:
                return

    def get_next_state(self):
        """
        Returns last element of de stack while removing it.
        """
        return self.stack.pop()

    def build_children(self, depth):
        """
        Get all the children of the input state and add them the dictionary.
        Creation of children are done by moving one car, checked for their
        uniqueness and depth, and adds them to the stack.
        """
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

                        # add child to list
                        self.stack.append((self.current_state, depth))

                        # save child in dictionary with (move, parent, depth)
                        self.children_parent_dict[current_occupation_hash] = \
                            ((vehicle.car, direction), parent_occupation_hash, \
                                 depth)

                        # solution if the red car is at the exit
                        if self.current_state.occupation[self.exit_tile] == \
                            self.red_car:
                            return True

                    # reset the current state as parent state for next child
                    self.current_state = copy.deepcopy(parent_state)

    def remove_deep_branches(self):
        for k, v in list(self.children_parent_dict.items()):
            if v[2] > self.max_depth:
                del self.children_parent_dict[k]

    def append_move_to_DataFrame_reversed(self, moves_df, move):
        """
        Appends the input move to the existing dataframe, saving the car name
        and the corresponding move.
        """
        # append move to DataFrame in reverse order since you start at the
        # winning state
        move_df = pd.DataFrame([[move[0], move[1]]], columns=['car name', \
            'move'])

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
        child_hash = hash(tuple(chain.from_iterable(child.occupation)))

        # search back in dict to find all the moves made to get to winning state
        while self.children_parent_dict[child_hash][0] != None:

            move, parent, _ = self.children_parent_dict[child_hash]
            child_hash = parent

            # put move into df
            self.moves_df = self.append_move_to_DataFrame_reversed(self.moves_df, move)

