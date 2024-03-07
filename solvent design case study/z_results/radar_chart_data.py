# This file is used to get the data needed for the Radar chart of the solvents

import pandas as pd
import numpy as np

def get_radarChart_data(x_complete):
    """
    TODO: to add
    Args:

    Return:

    """

    x = x_complete[:46]

    # Load the properties matrix Excel file into a DataFrame
    solvent_file = 'solvent_list_matrix.xlsx'
    solvent_prop_sheet = 'group_properties_formatted'
    prop_mat = pd.read_excel(solvent_file,sheet_name=solvent_prop_sheet,header=None)

    # Exclude the first row and first column
    df_prop = prop_mat.iloc[1:,1:]

    prop_mat = df_prop.to_numpy()

    acidity = 0.010641 + prop_mat[2,:]@x  # Agc
    if acidity <= 0.029:
        acidity = 0

    basicity = 0.12371 + prop_mat[3,:]@x # Bc
    if basicity <= 0.124:
        basicity = 0

    s_polarity = 0.325675 + prop_mat[4,:]@x # Sc

    Hv = 10.4327 + prop_mat[5,:]@x  # Hvc
    Vm = 0.0123 + prop_mat[6,:]@x  # Vmc
    R_const = 8.3145
    T_const = 298.15  # K
    delta_HSqr = 0.238846 * (Hv - 1e-3*R_const*T_const)/Vm

    # aromatic groups aCH,aC,aCCH3,aCCH2,aCCH,aCOH,aCNH2,aCCl,aCF
    indices_aromatic = [9, 10, 11, 12, 13, 15, 29, 36, 42]
    is_aromatic = x[indices_aromatic].sum()

    # non-aromatic halogen containing groups CH2Cl,CHCl,CHCl2,CHCl3,IO,Br
    h_iH = np.array([1,1,2,3,1,1]).reshape(-1,1)
    indices_nonAr_halogen = [32, 33, 34, 35, 40, 41]
    is_nonAr_halogen = x[indices_nonAr_halogen].reshape(1,-1).dot(h_iH)

    if is_aromatic > 0:
        delta_corr = 1
    elif is_nonAr_halogen >0:
        delta_corr = 0.5
    else:
        delta_corr = 0

    a = acidity
    b = basicity
    c = s_polarity
    d = delta_HSqr

    return a, b, c, d

def normalize_vector(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = (data - min_val) / (max_val - min_val)
    return normalized_data

def obtain_all_data():
    # Load the matrix Excel file into a DataFrame
    matrix_excel_file = 'solvent_list_generated_analysis_Dec06.xlsx'
    sheet_name_1 = 'row_data'
    matrix_df_solventList = pd.read_excel(matrix_excel_file, sheet_name=sheet_name_1,header=None)

    df_solventList = matrix_df_solventList.iloc[1:, 2:]
    matrix_solventList_full= df_solventList.to_numpy()
    num_iteration = matrix_solventList_full.shape[0]

    a = np.zeros((num_iteration,1))
    b = np.zeros((num_iteration,1))
    c = np.zeros((num_iteration,1))
    d = np.zeros((num_iteration,1))

    for i in range(num_iteration):
        a_i, b_i, c_i, d_i = get_radarChart_data(matrix_solventList_full[i,:])
        a[i, 0] = a_i
        b[i,0] = b_i
        c[i, 0] = c_i
        d[i, 0] = d_i

    a_norm = normalize_vector(a)
    b_norm = normalize_vector(b)
    c_norm = normalize_vector(c)
    d_norm = normalize_vector(d)

    combined = np.hstack((a_norm,b_norm,c_norm,d_norm)).squeeze()

    # return a_norm.flatten().tolist(), b_norm.flatten().tolist(), c_norm.flatten().tolist(), d_norm.flatten().tolist()
    # return a_norm, b_norm, c_norm, d_norm
    # return a.flatten().tolist(), b.flatten().tolist(), c.flatten().tolist(), d.flatten().tolist()
    return combined.tolist()

def obtain_top10_data():
    # Load the matrix Excel file into a DataFrame
    matrix_excel_file = 'solvent_list_generated_analysis_Dec06.xlsx'
    sheet_name_1 = 'top10'
    matrix_df_solventList = pd.read_excel(matrix_excel_file, sheet_name=sheet_name_1,header=None)

    df_solventList = matrix_df_solventList.iloc[1:, 2:]
    matrix_solventList_full= df_solventList.to_numpy()
    num_iteration = matrix_solventList_full.shape[0]

    a = np.zeros((num_iteration,1))
    b = np.zeros((num_iteration,1))
    c = np.zeros((num_iteration,1))
    d = np.zeros((num_iteration,1))

    for i in range(num_iteration):
        a_i, b_i, c_i, d_i = get_radarChart_data(matrix_solventList_full[i,:])
        a[i, 0] = a_i
        b[i,0] = b_i
        c[i, 0] = c_i
        d[i, 0] = d_i

    a_norm = normalize_vector(a)
    b_norm = normalize_vector(b)
    c_norm = normalize_vector(c)
    d_norm = normalize_vector(d)

    combined = np.hstack((a_norm,b_norm,c_norm,d_norm)).squeeze()

    # return a_norm.flatten().tolist(), b_norm.flatten().tolist(), c_norm.flatten().tolist(), d_norm.flatten().tolist()
    # return a_norm, b_norm, c_norm, d_norm
    # return a.flatten().tolist(), b.flatten().tolist(), c.flatten().tolist(), d.flatten().tolist()
    return combined.tolist()

# a, b, c, d = obtain_all_data()
# # Create a DataFrame
# data = pd.DataFrame({'a': a, 'b': b, 'c': c, 'd': d})
#
# # Specify the Excel file name
# excel_file_name = 'solvent_properties.xlsx'
#
# # Write the DataFrame to an Excel file
# data.to_excel(excel_file_name, index=False)