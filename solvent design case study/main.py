# run PWAS to solve the case study


from pwasopt.main_pwas import PWAS # pip install pwasopt; https://github.com/mjzhu-p/PWAS
from pwasopt.categorical_encoder import cat_encoder
import numpy as np
import pandas as pd
from qm_simulator import get_qm_calculatedValue


key = 0
np.random.seed(key)  # rng default for reproducibility

# solver related parameters
delta_E = 0.05  # trade-off hyperparameter in acquisition function between exploitation of surrogate and exploration of exploration function
acq_stage = 'multi-stage'  # can specify whether to solve the acquisition step in one or multiple stages (as noted in Section 3.4 in the paper [1]. Default: `multi-stage`
feasible_sampling = True  # can specify whether infeasible samples are allowed. Default True
K_init = 10  # number of initial PWA partitions

# optimization variables
nc = 0
nint = 46  # functional groups
nd = 1+ 3 + 3 +1 # m, binary variables yac, ybi, ymo, ysd_ac, ysd_acch, ysd_acch2, ymac
X_d = [3, 2, 2, 2, 2, 2, 2, 2]

# constraints
# Load the matrix Excel file into a DataFrame
matrix_excel_file = 'solvent_list_matrix.xlsx'
sheet_name_1 = 'str_ineq_const_toFormat'
sheet_name_2 = 'str_eq_const_toFormat'
sheet_name_3 = 'bounds_on_optVar'
matrix_df_ineq = pd.read_excel(matrix_excel_file, sheet_name=sheet_name_1,header=None)
matrix_df_eq = pd.read_excel(matrix_excel_file, sheet_name=sheet_name_2,header=None)
matrix_df_bd = pd.read_excel(matrix_excel_file, sheet_name=sheet_name_3,header=None)

# Exclude the first row and first column
df_ineq = matrix_df_ineq.iloc[1:, 1:]
df_eq = matrix_df_eq.iloc[1:, 1:]
df_bd = matrix_df_bd.iloc[1:, 1:]

# Replace NaN values with 0
with pd.option_context("future.no_silent_downcasting", True):
    # Included to ope with the FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version
    df_ineq = df_ineq.fillna(0).infer_objects(copy=False)
    df_eq = df_eq.fillna(0).infer_objects(copy=False)
    df_bd = df_bd.fillna(0).infer_objects(copy=False)

matrix_ineq = df_ineq.to_numpy()
matrix_eq = df_eq.to_numpy()
matrix_bd = df_bd.to_numpy()

Aineq = matrix_ineq[:, :-1]
bineq = matrix_ineq[:, -1].reshape(-1,1)

Aeq = matrix_eq[:, :-1]
beq = matrix_eq[:, -1].reshape(-1,1)

lb = matrix_bd[0,:]
ub = matrix_bd[1,:]

isLin_eqConstrained = True
isLin_ineqConstrained = True

preProcessingCatVar = True
if preProcessingCatVar:
    from pwasopt.formatCatVar import formatCatVar_encoded
    Aeq,Aineq = formatCatVar_encoded(nc,nint,nd,lb,ub,X_d,Aeq,Aineq,isLin_eqConstrained, isLin_ineqConstrained)


nsamp = 10
maxevals = 50


# isLin_eqConstrained = False
# isLin_ineqConstrained = False
# Aeq = np.array([])
# beq = np.array([])
# Aineq = np.array([])
# bineq = np.array([])

rxn_rate_simulator = get_qm_calculatedValue

# initialize the PWAS solver
optimizer1 = PWAS(rxn_rate_simulator, lb, ub, delta_E, nc, nint, nd, X_d, nsamp, maxevals,  # pass fun to PWAS
                 feasible_sampling= feasible_sampling,
                 isLin_eqConstrained=isLin_eqConstrained, Aeq=Aeq, beq=beq,
                 isLin_ineqConstrained=isLin_ineqConstrained, Aineq=Aineq, bineq=bineq,
                 K=K_init, categorical=False,
                 acq_stage=acq_stage, integer_cut=True)

xopt1, fopt1 = optimizer1.solve()
X1 = np.array(optimizer1.X)
fbest_seq1 = optimizer1.fbest_seq

out = optimizer1.result_output()
omega = out['omega']
gamma = out['gamma']
Kf = out['Kf']
a = out['a']
b = out['b']


# %% Save data
# find where x is in PWL partition
EC_cat = cat_encoder(out['self'].prob)
cat_encoder = EC_cat.cat_encoder()
X1_encoded = EC_cat.encode(X1,cat_encoder)
N_pt = X1_encoded.shape[0]
delta = np.argmax(X1_encoded[:,] @ omega[:,].T + gamma, axis=1)

# output the file solvent list to a separate Excel file
# Iterate through the NumPy arrays and create a row for each
import pandas as pd


rows = []
for gc in X1:
    row = list(gc)
    rows.append(row)

# # Convert the list of rows into a pandas DataFrame
# df_solvent_rows = pd.DataFrame(rows)

# Define the header row
header_row = [
    'CH3', 'CH2', 'CH', 'C', 'CH2dCH', 'CHdCH',
    'CH2dC', 'CHdC', 'CdC', 'aCH', 'aC', 'aCCH3', 'aCCH2', 'aCCH', 'OH', 'aCOH',
    'CH3CO', 'CH2CO', 'CHO', 'CH3COO', 'CH2COO', 'CH3O', 'CH2O', 'CH-O', 'CH2NH2',
    'CH3NH', 'CH2NH', 'CH3N', 'CH2N', 'aCNH2', 'CH3CN', 'CH2CN', 'CH2Cl', 'CHCl',
    'CHCl2', 'CHCl3', 'aCCl', 'CH2NO2', 'CHNO2', 'CH2SH', 'Io', 'Br', 'aCF', 'CH2S',
    'C2H6SO', 'C2H5NO', 'm', 'yac', 'ybi', 'ymo', 'ysd_ac', 'ysd_acch', 'ysd_acch2',
    'ymac'
]

# Create an empty DataFrame with the header row
df = pd.DataFrame(rows, columns=header_row)
df['QM/log k'] = [i * -1 for i in out['F']]
df['Partition'] = delta
df.insert(0, 'Iteration', None)
df.insert(1, 'Solvent Structure', None)

# Choose the filename and sheet name
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

filename = f'solvent_list_generated_{timestamp}.xlsx'
sheet_name = 'row_data'

# Export the DataFrame to an Excel file
df.to_excel(filename, sheet_name=sheet_name, index=False, engine='openpyxl')


# make a copy of the exisiting sheet
from openpyxl import load_workbook

row_data_copy = 'row_data_copy'
wb  = load_workbook(filename)
dup_ws = wb.copy_worksheet(wb["row_data"])
dup_ws.title = row_data_copy

wb.save(filename)

# To generate the solvent structure
df_toAnalyze = pd.read_excel(filename, sheet_name=row_data_copy, dtype=str)

# Iterate through the columns (excluding the first two)
for index, row in df_toAnalyze.iterrows():
    df_toAnalyze.iloc[index,1] = ''

    for col in df_toAnalyze.columns[2:48]:
        if int(float(row[col])) > 0:
            df_toAnalyze.iloc[index,1] += col + ' ' + str(int(float(row[col]))) + ' '


# update the solvent structure and update the Excel file
df['Solvent Structure'] = df_toAnalyze.iloc[:,1]
df.to_excel(filename, sheet_name=sheet_name, index=False, engine='openpyxl')

# df['Solvent Structure'] = df.iloc[:, 2:].sum(axis=1)


# # Save the updated DataFrame to a new Excel file if needed
# filename_solventStructure = filename[:-5] + '_solventStructure' + '.xlsx'
# df_toAnalyze.to_excel(filename_solventStructure, index=False)

# %%
# Following code can be used for data analysis, uncomment to use
#
# # check the predictability of the surrogate on the training data
# yhat = np.zeros((N_pt,1))
# yhat[:] = np.sum(a[delta,:,0] * X1_encoded, axis = 1).reshape((N_pt,1)) + b[delta]
# F_qm = np.array(out['F']).reshape(N_pt,1)
# ymean = np.sum(F_qm[:]) / N_pt
# # score_train = 1 - np.sum((F_qm[:] - yhat[:]) ** 2) / np.sum((F_qm[:] - ymean) ** 2)
# mse_train = np.sum((F_qm[:] - yhat[:]) ** 2)/N_pt

# check the predictability of the rest of the solvents
# Load the matrix Excel file into a DataFrame
# matrix_excel_file_ = 'solvent_pwas_reducedList.xlsx'
# sheet_name_1 = 'row_data'
# matrix_df_solventList = pd.read_excel(matrix_excel_file_, sheet_name=sheet_name_1,header=None)
#
# # Exclude the first row and first column
# df_solventList = matrix_df_solventList.iloc[1:, 2:]
# matrix_solventList_full= df_solventList.to_numpy()
# matrix_solventList = matrix_solventList_full[:, :-2]
# matrix_solventList_encoded = EC_cat.encode(matrix_solventList,cat_encoder).astype(int)
# matrix_solventList_encoded_str =np.array([str(row) for row in matrix_solventList_encoded])
# X1_encoded_str = np.array([str(row) for row in X1_encoded.astype(int)])
# rows_to_exclude = np.isin(matrix_solventList_encoded_str, X1_encoded_str, invert=True)
# matrix_solventList_untrained = matrix_solventList_encoded[rows_to_exclude]
# # matrix_solventList_untrained = matrix_solventList_encoded[~np.isin(matrix_solventList_encoded, X1_encoded).all(axis=1)]
# N_pt_untrained = matrix_solventList_untrained.shape[0]
# delta_untrained = np.argmax(matrix_solventList_untrained[:,] @ omega[:,].T + gamma, axis=1)
# y_hat_untrained =  np.zeros((N_pt_untrained,1))
# y_hat_untrained[:] = np.sum(a[delta_untrained,:,0] * matrix_solventList_untrained, axis = 1).reshape((N_pt_untrained,1)) + b[delta_untrained]
# F_qm_untrained = -matrix_solventList_full[rows_to_exclude, -2]
# ymean_untrained = np.sum(F_qm_untrained[:]) / N_pt_untrained
# # score_untrain = 1 - np.sum((F_qm_untrained[:] - y_hat_untrained[:]) ** 2) / np.sum((F_qm_untrained[:] - ymean_untrained) ** 2)
# mse_untrain = np.sum((F_qm_untrained[:] - y_hat_untrained[:]) ** 2)/N_pt_untrained
#
# mlr_pred = -matrix_solventList_full[rows_to_exclude, -1]
# ymean_untrained_mlr = np.sum(mlr_pred[:]) / N_pt_untrained
# # score_untrain_mlr = 1 - np.sum((F_qm_untrained[:] - mlr_pred[:]) ** 2) / np.sum((F_qm_untrained[:] - ymean_untrained_mlr) ** 2)
# mse_untrain_mlr = np.sum((F_qm_untrained[:] - mlr_pred[:]) ** 2)/N_pt_untrained


# # check the similarity among designed solvents (cosine similarity)
# def cosine_similarity(vec1, vec2):
#     vec1_norm = np.linalg.norm(vec1)
#     vec2_norm = np.linalg.norm(vec2)
#     return np.dot(vec1, vec2) / (vec1_norm * vec2_norm)
#
# def cosine_similarity_matrix(vectors):
#     return np.array([[cosine_similarity(vec1, vec2) for vec2 in vectors] for vec1 in vectors])
#
# similarity_matrix_solvent = cosine_similarity_matrix(X1)
