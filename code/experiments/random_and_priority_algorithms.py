import math
import copy
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from code.classes import board, game
from code.algorithms import dfs_hill_climber, randomise, priority_red_car, \
move_cars_in_way, depth_first, breath_first, randomise_move_more_squares


# -------- Test random algorithm to random with priority algorithm --------
random_moves_list = []
priority_moves_list = []

    # make lists into dataframe
    moves_to_solve_df = pd.DataFrame({'total moves random': random_moves_list, \
    'total moves priority': priority_moves_list})

    # save dataframe to csv
    moves_to_solve_df.to_csv(csv_output, index=False)

    # run random with priority algorithm
    test_game = game.Game(f"data/solutions/" + args.output_file, \
        copy.deepcopy(test_board), priority_red_car.move_priority_red_car)

    # append the number of moves it took to solve the board to list
    number_of_moves_prio = test_game.move_counter
    priority_moves_list.append(number_of_moves_prio)

# make lists into dataframe
moves_to_solve_df = pd.DataFrame({'total moves random': random_moves_list, \
'total moves priority': priority_moves_list})

# save dataframe to csv
moves_to_solve_df.to_csv(args.output_file, index=False)

# plot data to histplot with kernal density estimate
sns.histplot(moves_to_solve_df, kde=True)
plt.xlabel('Total number of moves to reach winning state')
plt.xlim(0, 50000)
plt.ylim(0, 115)
plt.title('Arrangement of total number of moves needed to solve board 6x6_2')
plt.savefig(f"data/graphs/" + args.output_png)
plt.show()
