import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ..helpers.colors  import cnames

class Visualisation():
    def __init__(self, board_csv, moves_csv):

        self.board_csv = board_csv
        self.moves_csv = moves_csv
        self.run()

    def run(self):
        self.read_csvs()
        self.get_gridsize()
        self.create_grid()
        self.move_cars()

    def read_csvs(self):
        self.df_board = pd.read_csv(self.board_csv)
        self.df_moves = pd.read_csv(self.moves_csv)

    def get_gridsize(self):
        """
        Returns the gridsize of the input file by using its file name
        """
        name_split = self.board_csv.split("Rushhour")[-1]
        self.grid_size = int(name_split.split("x")[0])

    def create_grid(self):

        # Create an empty 6x6 grid
        grid = np.zeros((self.grid_size, self.grid_size))

        # Populate the grid with the cars and their orientations
        for _, row in self.df_board.iterrows():
            car, orientation, col, row, length = row
            if orientation == 'H':
                for i in range(length):
                    grid[row-1][col-1+i] = ord(car)
            else:
                for i in range(length):
                    grid[row-1+i][col-1] = ord(car)

        # get unique characters
        car_types = np.unique(grid)

        # Plot the grid using matplotlib
        fig, ax = plt.subplots()

        # use the unique characters as the values for the colormap
        cmap = plt.get_cmap('prism')
        cmap.set_under(color='white')
        cmap.set_bad(color='white')
        cmap.set_over(color='white')

        ax.imshow(grid, cmap=cmap, origin='lower', extent=[0, self.grid_size, \
        0, self.grid_size], vmin=0, vmax=car_types.max())
        plt.pause(0.1)
        plt.show()

    def move_cars(self):
        for _,row in self.df_moves.iterrows():
            car, direction = row
            vehicle_row = self.df_board.loc[self.df_board['car'] == car]

            # Move the car based on the direction
            if direction == "left":
                vehicle_row['col'] -= 1
                self.df_board.loc[self.df_board['car'] == car, 'col'] = vehicle_row['col']
                self.create_grid()
            elif direction == "right":
                vehicle_row['col'] += 1
                self.df_board.loc[self.df_board['car'] == car, 'col'] = vehicle_row['col']
                self.create_grid()
            elif direction == "up":
                vehicle_row['row'] -= 1
                self.df_board.loc[self.df_board['car'] == car, 'row'] = vehicle_row['row']
                self.create_grid()
            elif direction == "down":
                vehicle_row['row'] += 1
                self.df_board.loc[self.df_board['car'] == car, 'row'] = vehicle_row['row']
                self.create_grid()

if __name__ == '__main__':
    board_csv = input('Enter the name of the board csv file: ')
    moves_csv = input('Enter the name of the moves csv file: ')
    Visualisation(board_csv, moves_csv)
