class Vehicles():
    def __init__(self, car, orientation, col, row, length, color):
        # get attributes
        self.car = car
        self.orientation = orientation
        self.positions = []
        self.length = length
        self.color = color

        # keep track of last move direction (ahead or back)
        self.movement = None
        # keep track of the vehicle(s) that the this vehicle is blocking and their direction
        self.blocking_veh = None
        # keep track of status of vehicle: it can move or it is being blocked
        self.status = "move"
        # keep track of future moves if one way (ahead/back) does not work
        self.future_move = None

        # keep track of the vehicle(s) that blocks this vehicle
        self.blocked_by = []

        # create a list of positions the vehicle occupies
        if orientation == "H":
            # positions for horizontal orientated vehicles
            for tile in range(length):
                self.positions.append((row, col + tile))
        else:
            # positions for vertical orietated vehicles
            for tile in range(length):
                self.positions.append((row + tile, col))