# This file is used to generate the heatmap of the solvent in terms of atom groups

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

matrix_excel_file = 'partition_analysis.xlsx'
sheet_name_combined = 'combined'

atom_groups = [
    r'CH$_3$', r'CH$_2$', 'CH', 'C', r'CH$_2$=CH', 'CH=CH',
    r'CH$_2$=C', 'CH=C', 'C=C', 'aCH', 'aC', r'aCCH$_3$', r'aCCH$_2$', 'aCCH', 'OH', 'aCOH',
    r'CH$_3$CO', r'CH$_2$CO', 'CHO', r'CH$_3$COO', r'CH$_2$COO', r'CH$_3$O', r'CH$_2$O', 'CH-O', r'CH$_2$NH$_2$',
    r'CH$_3$NH', r'CH$_2$NH', r'CH$_3$N', r'CH$_2$N', r'aCNH$_2$', r'CH$_3$CN', r'CH$_2$CN', r'CH$_2$Cl', 'CHCl',
    r'CHCl$_2$', r'CHCl$_3$', 'aCCl', r'CH$_2$NO$_2$', r'CHNO$_2$', r'CH$_2$SH', 'I', 'Br', 'aCF', r'CH$_2$S',
    r'C$_2$H$_6$SO', r'C$_2$H$_5$NO'
]

combined_data = pd.read_excel(matrix_excel_file, sheet_name=sheet_name_combined).iloc[0:, 1:]

# Sort the DataFrame by the partition column for better visualization
data_sorted = combined_data.sort_values(by='partition')

# Extract the partition labels
partitions = data_sorted['partition'].unique()

# Extract all features
all_features = combined_data.columns[:-1]  # Exclude the partition column
all_data = combined_data[all_features]

all_features_sorted = data_sorted.columns[:-1]  # Exclude the partition column
all_data_sorted = data_sorted[all_features_sorted]

# # Extract the last four features
# last_four_features = data_sorted.columns[-4:-1]
# last_four_data = data_sorted[last_four_features]

other_data_features = all_data.columns[:-4]
other_data = all_data[other_data_features]

other_data_features_sorted = all_data_sorted.columns[:-4]
other_data_sorted = data_sorted[other_data_features_sorted]

# Create subplots with 1 row and 2 columns
fig, (ax1, ax2, cbar_ax) = plt.subplots(nrows=3,ncols=1, figsize=(12, 16),
                                        gridspec_kw={"height_ratios":[1, 1, 0.03]})

# Heatmap 1: ordered in iteration
cmap = 'YlGnBu'

sns.heatmap(other_data, cmap=cmap, xticklabels =atom_groups, yticklabels=all_data.index+1, ax=ax1, cbar=False)
ax1.axhline(10, color='black', linewidth=2)

# ax1.set_title('Sequential Iteration Order', fontsize=12, fontweight='bold')
ax1.tick_params(labelsize = 10)
ax1.set_ylabel('Iterations in sequential order', fontsize =13)
ax1.set_xlabel('Atom groups', fontsize =13)

# Heatmap 2: ordered in partition
im = sns.heatmap(other_data_sorted, cmap=cmap, xticklabels =atom_groups, yticklabels=other_data_sorted.index+1, ax=ax2,cbar=False)
# Highlight the partition boundaries on heatmap 1
for i, partition in enumerate(partitions):
    if i > 0:
        ax2.axhline(data_sorted[data_sorted['partition'] == partition].index[0], color='darkorange', linewidth=2)
# ax2.set_title('Grouped in Partitions', fontsize=12, fontweight='bold')
ax2.tick_params(labelsize = 10)
ax2.set_ylabel('Iterations grouped in partitions', fontsize =13)




# cbar_ax = fig.add_axes([0.01, 0.06, 0.9, 0.02])
cbar_ax.tick_params(labelsize = 10)
# cbar_ax.set_label('Number of each atom group in the solvent')
mappable = im.get_children()[0]
cbar1 = plt.colorbar(mappable,cax=cbar_ax, orientation="horizontal")
cbar1.set_label('Number of each atom group in the solvent',fontsize = 13)

# axes.set_title('Group contributions')
# plt.subplots_adjust(right=0.99)
# Duplicate the y-axis ticks on the right side of the plot
# plt.axis('tight')



# plt.suptitle('Side-by-Side Heatmaps of Samples and Features with Partition Boundaries (Normalized)')
# plt.show()
plt.tight_layout()
plt.savefig('heatmap_solvent.pdf', dpi=400,bbox_inches='tight', pad_inches=0.03)
plt.savefig('heatmap_solvent.png', dpi=400,bbox_inches='tight', pad_inches=0.03)