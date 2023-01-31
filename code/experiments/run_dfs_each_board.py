"""
Runs the depth-first search for each board, save the results and export to a
csv-file.
"""
import pandas as pd

from ..code.algorithms import depth_first
from ..code.classes import board, game

data_dfs = []

boards = ["6x6_1", "6x6_2","6x6_3", "9x9_4", "9x9_5", "9x9_6", "12x12_7"]
for board_nr in boards :
    # create initial board
    test_board = board.Board(f"data/gameboards/" + f"Rushhour{board_nr}.csv")

    # run algorithm
    test_game = game.Game(f"data/solutions/" + f"dfs_{board_nr}.csv",
        test_board,
        depth_first.Depth_First_Search,
        first_search=True)

    # save results
    data_dfs.append(
        {"board": board_nr,
        "number_of_states": test_game.nr_states,
        "number_of_moves": test_game.moves_df.shape[0]}
    )

# to dataframe
df_data_dfs = pd.DataFrame(data_dfs)
# export to csv file
df_data_dfs.to_csv("data/DFS_each_board.csv", index=False)
