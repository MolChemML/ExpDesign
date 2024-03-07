# This file is used to generate the heatmap of all the solvent that are feasible within the design space

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

matrix_excel_file = 'partition_analysis.xlsx'
sheet_name_combined = 'wholeFeasible'

combined_data = pd.read_excel(matrix_excel_file, sheet_name=sheet_name_combined).iloc[0:, 1:]


# Extract all features including the last four
all_features = combined_data.columns[:-1]  # Exclude the partition column
all_data = combined_data[all_features]


# # Extract the last four features
# last_four_features = data_sorted.columns[-4:-1]
# last_four_data = data_sorted[last_four_features]

other_data_features = all_data.columns[:]
other_data = all_data[other_data_features]


# Create subplots with 1 row and 2 columns
fig, (ax1, cbar_ax) = plt.subplots(nrows=2,ncols=1, figsize=(20, 35),
                                        gridspec_kw={"height_ratios":[1, 0.005]})

# Heatmap 1: ordered in iteration
cmap = 'YlGnBu'
im = sns.heatmap(other_data, cmap=cmap, yticklabels=all_data.index+1, ax=ax1, cbar=False)
# ax1.axhline(10, color='black', linewidth=2)

# ax1.set_title('Sequential Iteration Order', fontsize=12, fontweight='bold')
ax1.tick_params(labelsize = 7)




# cbar_ax = fig.add_axes([0.01, 0.06, 0.9, 0.02])
cbar_ax.tick_params(labelsize = 7)
mappable = im.get_children()[0]
plt.colorbar(mappable,cax=cbar_ax, orientation="horizontal")

# axes.set_title('Group contributions')
# plt.subplots_adjust(right=0.99)
# Duplicate the y-axis ticks on the right side of the plot
# plt.axis('tight')



# plt.suptitle('Side-by-Side Heatmaps of Samples and Features with Partition Boundaries (Normalized)')
# plt.show()
plt.tight_layout()
plt.savefig('heatmap_solvent_Feasible.pdf', dpi=400,bbox_inches='tight', pad_inches=0.03)
plt.savefig('heatmap_solvent_Feasible.png', dpi=400,bbox_inches='tight', pad_inches=0.03)