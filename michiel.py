import tkinter as tk
import matplotlib.colors as mlc

# create a 6x6 grid of grey squares
def create_grid(root):
    grid = []
    for i in range(6):
        row = []
        for j in range(6):
            square = canvas.create_rectangle(j*100, i*100, (j+1)*100, (i+1)*100, fill='dimgrey')
            row.append(square)
        grid.append(row)
    return grid

# Update the color of a square
def update_square(square, color):
    canvas.itemconfig(square, fill=color)

# Create the main window
root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

grid = create_grid(root)

#Update one of the square
update_square(grid[2][2], 'red')
# update_square(grid[2][3], 'red')
# update_square(grid[3][2], 'red')
# update_square(grid[2][1], 'red')


root.mainloop()
