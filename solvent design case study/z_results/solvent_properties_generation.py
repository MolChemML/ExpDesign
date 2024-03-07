# This file is used to generate solvent properties data based on GC method

import pandas as pd
import numpy as np

# TODO: add comments and notes

def lookup_properties_and_save(lookup_file_path, lookup_sheet_name, keys_file_path, keys_sheet_names, key_column_name, properties_column_names, output_file_path):
    # Load the lookup table from the specified sheet in the Excel file
    lookup_table = pd.read_excel(lookup_file_path, sheet_name=lookup_sheet_name)

    # Create an Excel writer to save the results to the output file
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        # Loop through each sheet in the keys spreadsheet
        for keys_sheet_name in keys_sheet_names:
            # Load the keys table from the specified sheet in the Excel file
            keys_table = pd.read_excel(keys_file_path, sheet_name=keys_sheet_name)

            # Merge the tables based on the key_column_name
            merged_table = pd.merge(keys_table, lookup_table, how='left', left_on=key_column_name, right_on=key_column_name)

            # Extract the key column and the desired properties columns
            result_subset = merged_table[[key_column_name] + properties_column_names]

            # Rename columns to include the sheet name
            result_subset.columns = [key_column_name] + [f"{col}" for col in properties_column_names]

            # Save the result to a new sheet in the output Excel file
            result_subset.to_excel(writer, sheet_name=f'Result_{keys_sheet_name}', index=False)

    print(f"Results have been saved to {output_file_path} in separate sheets.")
    return None

lookup_file_path = 'solvent_properties_gc.xlsx'
# lookup_sheet_name = 'radarChart'
lookup_sheet_name = 'SS2(CAMD)'
keys_file_path = 'solvent_list_generated_analysis_Dec06.xlsx'
keys_sheet_names = ['row_data', 'top10']
key_column_name = 'Solvent Structure'  # Replace with the actual column name in your keys table
properties_column_names = ['n_square', 'A', 'B', 'Gamma','Epsilon', 'Aromaticity','Halogenicity', 'lnk_QM']  # Replace with the actual property column names
output_file_path = 'Solvent_properties_generated_allFeatures.xlsx'


result_df = lookup_properties_and_save(lookup_file_path, lookup_sheet_name, keys_file_path, keys_sheet_names, key_column_name, properties_column_names, output_file_path)

print(f"Results have been saved to {output_file_path}")



