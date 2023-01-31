import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("data/gameboards_different_max_depth_DLS2.csv")
sns.scatterplot(x='max_depth', y='number_of_states', hue='board', data=df)
plt.show()
plt.savefig('6x6_diff_max_depth.png')
