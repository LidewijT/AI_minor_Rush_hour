"""
In this file we will simulate the game of rush hour
"""
# import functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
        self.vehicle_list.append(Vehicles(car, orientation, col, row, length))

for vehicle in gameboard_df.iterrows():
    Board().add_vehicles(vehicle[1]['car'], vehicle[1]['orientation'], vehicle[1]['col'], vehicle[1]['row'], vehicle[1]['length'])

plt.plot([0,1,2], [1, 2, 3])
plt.grid(visible=True)
plt.show()
