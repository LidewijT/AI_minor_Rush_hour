import copy
from itertools import chain

from .depth_limited import Depth_Limited_Search
from ..classes.board import Board

class DFS_Hill_Climber(Depth_Limited_Search):
    """
    This class is similar to the depth-limited search and depth-first search
    algorithm. The depth-first search with hill climber algorithm finds a
    solution according the depth-first search, and then optimises this by
    resetting the maximum depth. After finding the optimal solution, it will
    start backtracking the moves into a dataframe.
    """

    def __init__(self, start_state, max_depth):
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

        self.solution_found = False
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
        if self.solution_found == True:
            self.moves_to_df(self.solution)
            self.won = True


    def build_children(self, depth):
        """
        Gets all the children of the input state and adds them the dictionary.
        Creation of children are done by moving one car, checked for their
        uniqueness and depth, and adds them to the stack.
        """
        # save parent state
        parent_state = copy.copy(self.current_state)

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
                        chain.from_iterable(self.current_state)))

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
                            self.solution_found = True

                            # save new, best created solution
                            self.solution = self.current_state

                            # reset max depth for better solutions
                            self.max_depth = depth

                            # remove deeper branches than new max_depth
                            self.remove_deep_branches()

                        # add child to stack
                        self.stack.append((self.current_state, depth))

                    # reset the current state as parent state for next child
                    self.current_state = copy.copy(parent_state)

    def remove_deep_branches(self):
        """
        Removes keys in the children_parent_dict when the corresponding depth
        exceeds the current maximum depth.
        """
        for k, v in list(self.children_parent_dict.items()):
            if v[2] > self.max_depth:
                del self.children_parent_dict[k]