"""
In this file we will simulate the game of rush hour
"""

# read csv


# initiate the classes
class Vehicles():
    def __init__(self, orientation, col, row, length):
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length

class Board():
    def __init__(self):
        self.vehicle_list = []

    def add_vehicles(self, orientation, col, row, length):
        vehicle_list.append(Vehicles(orientation, col, row, length))
