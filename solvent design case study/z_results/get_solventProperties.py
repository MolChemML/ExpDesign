
import pandas as pd
import numpy as np
def get_solventProperties_(x_complete):
    """
    Used to calculate solvent properties based on group contribution method of Sheldon et al, 2005

    """

    x = x_complete.values

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

    return acidity, basicity, s_polarity, delta_corr, delta_HSqr




# Load the original data
file_path = 'solvent_list_matrix.xlsx'
sheet_name = 'Menschutkin_full_design_space'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Extract the features from the DataFrame
features_df = df.iloc[:, 2:-1]


# Apply the function to each row
properties_df = features_df.apply(get_solventProperties_, axis=1, result_type='expand')
properties_df.columns = ['acidity', 'basicity', 's_polarity', 'delta_corr', 'delta_HSqr']

# Save the new spreadsheet with calculated properties
output_file_path = 'calculated_properties.xlsx'
properties_df.to_excel(output_file_path, index=False)
