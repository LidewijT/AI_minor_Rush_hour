class Vehicles():
    """
    This class represents the individual vehicles in the game Rush Hour, which
    includes several attributes and are initialised in the 'init' method. These
    define the behaviour of the vehicle within the game.
    """

    def __init__(self, car, orientation, col, row, length, number):
        """
        Initializes all attributes of the class with its parameters. It uses its
        starting position (row, col) and length to determine all squares
        occupied by the vehicle based on its orientation.
        """
        # get attributes
        self.car = car
        self.orientation = orientation
        self.positions = []
        self.length = length
        self.number = number

        # create a list of tuples to store the positions the vehicle occupies
        if orientation == "H":
            # positions for horizontal orientated vehicles
            for tile in range(length):
                self.positions.append((row, col + tile))
        else:
            # positions for vertical orientated vehicles
            for tile in range(length):
                self.positions.append((row + tile, col))
