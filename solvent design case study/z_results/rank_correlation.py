# This file is used to check the rank correlation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
def plot_rank(x,y, ax=None, color=None):
    if ax is None:
        fig, ax = plt.subplots()

    ax.scatter(x, y, color=color, marker='o',zorder = 11, s=25)



# %%
matrix_excel_file = 'rank_analysis.xlsx'
sheet_name_pwas = 'rank'
qm_df = np.array(pd.read_excel(matrix_excel_file, sheet_name = sheet_name_pwas).iloc[0, 1:])
mlr_df = np.array(pd.read_excel(matrix_excel_file, sheet_name = sheet_name_pwas).iloc[1, 1:])
pwas_df = np.array(pd.read_excel(matrix_excel_file, sheet_name = sheet_name_pwas).iloc[2, 1:])


# %%

fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))


plot_rank(qm_df,mlr_df, ax=ax, color='#0e4581')

ax.set_ylabel('Rank - MLR', fontsize=14)
ax.set_xlabel('Rank - QM', fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.grid(linestyle=":")

plt.tight_layout()
plt.savefig('rank_qm_mlr_whole.png', dpi=400)
plt.savefig('rank_qm_mlr_whole.pdf', dpi=400)

# %%

fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))


plot_rank(qm_df,mlr_df, ax=ax, color='#0e4581')

ax.set_ylabel('Rank - MLR', fontsize=14)
ax.set_xlabel('Rank - QM', fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)

ax.set_yticks(range(1, 15, 1))
ax.set_xticks(range(1, 11, 1))
ax.set_xlim(0, 11)
ax.set_ylim(0, 15)

ax.grid(linestyle=":")

plt.tight_layout()
plt.savefig('rank_qm_mlr_top10.png', dpi=400)
plt.savefig('rank_qm_mlr_top10.pdf', dpi=400)

# %%

fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))


plot_rank(qm_df,pwas_df, ax=ax, color='#0e4581')

ax.set_ylabel('Rank - PWAS', fontsize=14)
ax.set_xlabel('Rank - QM', fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.grid(linestyle=":")

plt.tight_layout()
plt.savefig('rank_qm_pwas_whole.png', dpi=400)
plt.savefig('rank_qm_pwas_whole.pdf', dpi=400)

# %%

fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))


plot_rank(qm_df,pwas_df, ax=ax, color='#0e4581')

ax.set_ylabel('Rank - PWAS', fontsize=14)
ax.set_xlabel('Rank - QM', fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)

ax.set_yticks(range(1, 15, 1))
ax.set_xticks(range(1, 11, 1))
ax.set_xlim(0, 11)
ax.set_ylim(0, 15)

ax.grid(linestyle=":")

plt.tight_layout()
plt.savefig('rank_qm_pwas_top10.png', dpi=400)
plt.savefig('rank_qm_pwas_top10.pdf', dpi=400)