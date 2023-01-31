""""
For all three 6x6 boards, it does a depth-limited search for different max
depth values, saves this data in a csv file and creates a graph with the number
of states for each max depth for each board.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from ..code.algorithms import depth_limited
from ..code.classes import board, game

data_dls = []

for board_nr in ["6x6_1", "6x6_2","6x6_3"]:
    test_board = board.Board(f"data/gameboards/" + f"Rushhour{board_nr}.csv")

    for max_depth in range(0, 1100, 20):
        print(
            f"\nDepth-limited Search, {board_nr}, with max-depth: {max_depth}"
        )
        # run algorithm with corresponding max_depth
        test_game = game.Game(
            f"data/solutions/" + "dfs_lim_" + str(max_depth) +"_6x6_1.csv",
            test_board,
            depth_limited.Depth_Limited_Search,
            first_search=True,
            max_depth=max_depth,
            create_csv=False
        )

        # save results
        if test_game.win == True:
            data_dls.append({
                "board": board_nr,
                "max_depth": max_depth,
                "number_of_states": test_game.nr_states,
                "number_of_moves": test_game.moves_df.shape[0]
            })

        else:
            data_dls.append(
                {"board": board_nr,
                "max_depth": max_depth,
                "number_of_states": test_game.nr_states,
                "number_of_moves": 0}
            )

# to dataframe
df_data_dls = pd.DataFrame(data_dls)
# export dataframe to csv file
df_data_dls.to_csv("data/gameboards_different_max_depth_DLS2.csv", index=False)

# create graph
sns.scatterplot(
    x='max_depth',
    y='number_of_states',
    hue='board',
    data=df_data_dls
)

# save graph
plt.savefig('6x6_diff_max_depth.png')