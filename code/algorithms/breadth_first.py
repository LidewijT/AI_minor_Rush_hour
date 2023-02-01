from .depth_first import Depth_First_Search

class Breadth_First_Search(Depth_First_Search):
    """
    This class computes the breadth-first search algorithm and works almost
    simlar to its superclass: DepthFirst. The only change is what state is
    retrieved from the stack. With breadth-first search is is te first that in
    the stack. This way, the exploration is done in the width and will return
    the optimal solution (minimal number of moves).
    """

    def get_next_state(self):
        """
        Returns the first element of the stack while removing it at the same
        time.
        """
        return self.stack.pop(0)
