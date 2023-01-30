import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Histogram():
    def __init__(self):


        self.plot()

    def make_df(self):
        moves_to_solve_df = pd.DataFrame({'total moves random': random_moves_list, \
        'total moves priority': priority_moves_list})

    def plot(self):
        # plot data to histplot with kernal density estimate
        sns.histplot(moves_to_solve_df, kde=True)
        plt.xlabel('Total number of moves to reach winning state')
        plt.xlim(0, 50000)
        plt.ylim(0, 115)
        plt.title('Arrangement of total number of moves needed to solve board 6x6_2')
        plt.savefig(f"data/graphs/" + args.output_png)
        plt.show()
