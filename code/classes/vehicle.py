class Vehicles():
    def __init__(self, car, orientation, col, row, length, color):
        # get attributes
        self.car = car
        self.orientation = orientation
        self.positions = []
        self.length = length
        self.color = color
        self.last_move = None

        # create a list of positions the vehicle occupies
        if orientation == "H":
            # positions for horizontal orientated vehicles
            for tile in range(length):
                self.positions.append((row, col + tile))
        else:
            # positions for vertical orietated vehicles
            for tile in range(length):
                self.positions.append((row + tile, col))