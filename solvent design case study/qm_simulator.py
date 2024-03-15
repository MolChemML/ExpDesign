# Return the ln(k) value given the structure of the solvent

import pandas as pd
import numpy as np
import sys


def get_qm_calculatedValue(x_complete):
    """

    Args:
        x_complete: optimization vector (the first 46 entries of x_complete[i] indicates the number of ith group in each selected solvent
        UNIFAC groups: CH3,CH2,CH,C,CH2dCH,CHdCH,CH2dC,CHdC,CdC,aCH,aC,aCCH3,aCCH2,aCCH,OH,aCOH,CH3CO,
                        CH2CO,CHO,CH3COO,CH2COO,CH3O,CH2O,CH-O,CH2NH2,CH3NH,CH2NH,CH3N,CH2N,aCNH2,CH3CN,
                        CH2CN,CH2Cl,CHCl,CHCl2,CHCl3,aCCl,CH2NO2,CHNO2,CH2SH,Io,Br,aCF,CH2S,C2H6SO,C2H5NO

    Return:
        ln(k) value calculated using quantum mechanical method (Reference: Gui, 2023)
    """

    x = np.round(x_complete[:46],decimals=1)

    # Load the matrix Excel file into a DataFrame
    matrix_excel_file = 'solvent_list_matrix_get_lnk_QM.xlsx'
    sheet_name = 'Menschutkin_full_design_space'
    matrix_df = pd.read_excel(matrix_excel_file, sheet_name = sheet_name)
    matching_qm_values = []

    # Iterate through the matrix rows and check for a match
    for index, row in matrix_df.iterrows():
        row_array = np.array(row[2:-1])  # Exclude the 'Cell Number', 'Solvent Structure' and 'QM' columns
        if np.array_equal(row_array, x):
            matching_qm_values = row['QM/log k']
            break


    if matching_qm_values == []:
        # # TODO: later, link some methods to calculate it (e.g. GC with MLR model) or set it to a pre-defined value
        # errstr = "The reaction rate for [" + str(x) + " ]" + "has not been calculated using quantum mechanical method."
        # print(errstr)
        # sys.exit(1)

        from gc_lnkCal import get_gc_rxn_Rate

        matching_qm_values = get_gc_rxn_Rate(x)

        # add the newly calculated value to the spreadsheet
        new_row_gc =  pd.Series(['gc', 'tbd'] + x.tolist() + [matching_qm_values], index=matrix_df.columns)

        # Append the new row to the existing DataFrame
        matrix_df = matrix_df.append(new_row_gc, ignore_index=True)

        # Save the updated DataFrame
        matrix_df.to_excel(matrix_excel_file, sheet_name = sheet_name, index=False)


    return -matching_qm_values
