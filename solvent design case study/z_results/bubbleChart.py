import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Read data from Excel file
excel_file = "Solvent_properties_generated.xlsx"
sheet_name_1 = "3d_plot"
# sheet_name_2 = "3d_plot_top10"

df1 = pd.read_excel(excel_file, sheet_name=sheet_name_1)
# df2 = pd.read_excel(excel_file, sheet_name=sheet_name_2)

# Extract data from the first sheet (3d_plot)
X1 = df1.iloc[:, -4].values
Y1 = np.log10(df1.iloc[:, -2].values)
Z1 = df1.iloc[:, -3].values
W1 = df1.iloc[:, -1].values


# Create a 1x2 subplot grid with a larger subplot in the first row, second column
fig, (ax1, cbar_ax) = plt.subplots(nrows=2, ncols=1, figsize=(13, 8.5),
                              gridspec_kw={"height_ratios":[1, 0.03]})

# Subplot 1: 2D Bubble Chart for the first data set
scatter1 = ax1.scatter(X1, Y1, s=(Z1 + .1) * 450, c=W1, cmap='viridis', alpha=1, edgecolors='black', linewidth=0.5)
ax1.grid()
ax1.set_xlabel("$n^2$", fontsize=14, fontweight='bold')
ax1.set_ylabel("$log\epsilon$", fontsize=15, fontweight='bold')
ax1.tick_params(axis='both', labelsize=13)  # Increase tick label font size
ax1.set_xlim(2.0,2.65)
ax1.set_ylim(-2.2, 0.4)



def annotate_plot(X,Y,W,ax):
    # Annotate each point with its rank
    # for i, txt in enumerate(range(1, len(X) + 1)):
    #     # if i
    #     ax.annotate(txt, (X[i], Y[i]), fontsize=7, ha='center', va='center', color='black')
    for i in range(len(X)):
        if W[i] >39:
            if W[i] in [49,47,41,43,42,40,44]:
                ax.annotate(str(W[i]), (X[i], Y[i]-0.1), fontsize=13, ha='center', va='center', color='black')
            elif W[i] in [48]:
                ax.annotate(str(W[i]), (X[i], Y[i]-0.11), fontsize=13, ha='center', va='center', color='black')
            elif W[i] in [45]:
                ax.annotate(str(W[i]), (X[i]+0.01, Y[i]-0.1), fontsize=13, ha='center', va='center', color='black')
            elif W[i] in [46]:
                ax.annotate(str(W[i]), (X[i] - 0.01, Y[i] - 0.1), fontsize=13, ha='center', va='center', color='black')
            elif W[i] in [50]:
                ax.annotate(str(W[i]), (X[i] + 0.015, Y[i]), fontsize=13, ha='center', va='center', color='black')
            else:
                ax.annotate(str(W[i]), (X[i], Y[i]), fontsize=13, ha='center', va='center', color='black')

        elif W[i] <11:
            if W[i] in [6]:
                ax.annotate(str(W[i]), (X[i]-0.005, Y[i]-0.1), fontsize=13, ha='center', va='center', color='black')
            elif W[i] in [5]:
                ax.annotate(str(W[i]), (X[i]+0.005, Y[i]-0.1), fontsize=13, ha='center', va='center', color='black')
            elif W[i] in [8]:
                ax.annotate(str(W[i]), (X[i] - 0.005, Y[i] + 0.1), fontsize=13, ha='center', va='center',
                            color='black')
            elif W[i] in [7]:
                ax.annotate(str(W[i]), (X[i] + 0.005, Y[i] +0.1), fontsize=13, ha='center', va='center',
                            color='black')
            else:
                ax.annotate(str(W[i]), (X[i], Y[i]), fontsize=13, ha='center', va='center', color='yellow')

annotate_plot(X1,Y1,W1,ax1)
# annotate_plot(X1,Y1,W1,ax2)
# annotate_plot(X1,Y1,W1,zoomed_axes_4)
# annotate_plot(X1+0.001,Y1,W1,zoomed_axes_2)


#
tick_list = [1,10,20,30,40,50]
cbar1 = plt.colorbar(scatter1, cbar_ax, ticks =tick_list, orientation="horizontal")
cbar1.set_label(r'Relative rank of the determined solvents by $PWAS$', fontsize=13)
cbar1.ax.tick_params(labelsize=13)
# cbar1.ax.set_xticklabels(['1', '10', '20', '30', '40', '50'])
# bubble_to_show = [0,0.15,0.30,0.45,0.60,0.75]
# bubble_to_show_2 = [(x + 0.1) * 450 for x in bubble_to_show]

# handles = scatter1.legend_elements(num=bubble_to_show_2)[0]  # extract the handles from the existing scatter plot

# ax1.legend(title='Basicity', handles=handles, labels={'0','0.15','0.30','0.45','0.60','0.90'},loc = 'lower right')
kw = dict(prop="sizes", num=6, fmt=" {x:.2f}",
          func=lambda s: (s/450)-0.1,color = 'r')
legend2 = ax1.legend(*scatter1.legend_elements(**kw),
                    title="Basicity",title_fontsize=12.5, fontsize = 12.5, loc="lower right",labelspacing=2,
                   frameon=True)

#
# cbar2 = plt.colorbar(scatter2, ax=ax1[1])
# cbar2.set_label(df2.columns[-1], fontsize=16)
# cbar2.ax.tick_params(labelsize=14)  # Increase colorbar tick label font size

# Adjust layout
plt.tight_layout()

# Save the figure with bbox_extra_artists parameter
plt.savefig('bubble_chart.png', orientation='landscape', dpi=400, pad_inches=0.03)
plt.savefig('bubble_chart.pdf', orientation='landscape', dpi=400, pad_inches=0.03)

# Show the plot
plt.show()



