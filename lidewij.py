"""
In this file we will simulate the game of rush hour
"""
# import functions
import pandas as pd

# read csv
gameboard_df = pd.read_csv("gameboards\Rushhour6x6_1.csv")
print(gameboard_df)

# initiate the classes
class Vehicles():
    def __init__(self, car, orientation, col, row, length):
        self.car = car
        self.orientation = orientation
        self.col = col
        self.row = row
        self.length = length

class Board():
    def __init__(self):
        self.vehicle_list = []

    def add_vehicles(self, car, orientation, col, row, length):
        print("test")
        self.vehicle_list.append(Vehicles(car, orientation, col, row, length))

for vehicle in gameboard_df.iterrows():
    print(vehicle[1]['car'], vehicle[1]['orientation'],vehicle[1]['col'],vehicle[1]['row'], vehicle[1]['length'])
    Board().add_vehicles(vehicle[1]['car'], vehicle[1]['orientation'], vehicle[1]['col'], vehicle[1]['row'], vehicle[1]['length'])
