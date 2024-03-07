# This file is used to perform the PDP and ICE analysis

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

# Load data from the Excel file
file_path = 'pdp_ice_data.xlsx'
sheet_name = 'row_data_wholeFeasibleDomain'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Extract features and target variable
X = df.iloc[:, 1:-1].values  # Assuming features are in columns 2 to second last columns
y = df.iloc[:, -1].values    # Assuming the last column is the prediction

# Extract feature names
# feature_names = df.columns[1:-1].tolist()
feature_names = ["$n^2$", "$A$", "$B$", "$\gamma$", "$\epsilon$", "$Aromaticity$", "$Halogenicity$"]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit a decision tree regression model
model = DecisionTreeRegressor()
model.fit(X_train, y_train)

# Function to calculate PDP for a given feature
def calculate_pdp(model, feature_values, feature_idx, X):
    predictions = []
    for value in feature_values:
        X_pdp = X.copy()
        X_pdp[:, feature_idx] = value
        predictions.append(np.mean(model.predict(X_pdp)))
    return np.array(predictions)

# Set up subplots
num_features = X.shape[1]

# Generate PDP and ICE plots for each feature
fig, axes = plt.subplots(ncols= 2, nrows= 4, figsize=(8, 8))
fig.delaxes(axes[3,0])
axes = axes.flatten()

for feature_idx in range(num_features):
    # Generate values for the chosen feature
    feature_values = np.linspace(np.min(X[:, feature_idx]), np.max(X[:, feature_idx]), 100)

    # Calculate PDP
    pdp_values = calculate_pdp(model, feature_values, feature_idx, X)

    # Calculate ICE
    ice_values = np.zeros((X.shape[0], len(feature_values)))
    for i, value in enumerate(feature_values):
        X_ice = X.copy()
        X_ice[:, feature_idx] = value
        ice_values[:, i] = model.predict(X_ice)

    # Plot PDP and ICE on the same subplot
    for i in range(ice_values.shape[0]):
        if feature_idx == num_features-1:
            if i ==ice_values.shape[0]-1:
                axes[feature_idx + 1].plot(feature_values, ice_values[i, :], color='gray', alpha=0.1,label=f'ICE for {feature_names[feature_idx]}')
            else:
                axes[feature_idx+1].plot(feature_values, ice_values[i, :], color='gray', alpha=0.1)
        else:
            if i ==ice_values.shape[0]-1:
                axes[feature_idx].plot(feature_values, ice_values[i, :], color='gray', alpha=0.1,label=f'ICE for {feature_names[feature_idx]}')
            else:
                axes[feature_idx].plot(feature_values, ice_values[i, :], color='gray', alpha=0.1)
    if feature_idx == num_features - 1:
        axes[feature_idx+1].plot(feature_values, pdp_values, label=f'PDP for {feature_names[feature_idx]}', color='red',
                               linestyle='dashed')
    else:
        axes[feature_idx].plot(feature_values, pdp_values, label=f'PDP for {feature_names[feature_idx]}', color='red', linestyle='dashed')

    # Customize subplot aesthetics
    if feature_idx == num_features - 1:
        axes[feature_idx+1].set_xlabel(f'{feature_names[feature_idx]}')
        axes[feature_idx+1].set_ylabel('lnk')
        # axes[feature_idx].set_title(f'PDP and ICE for {feature_names[feature_idx]}')
        axes[feature_idx+1].legend(loc='lower right', frameon=False)
    else:
        axes[feature_idx].set_xlabel(f'{feature_names[feature_idx]}')
        axes[feature_idx].set_ylabel('lnk')
        # axes[feature_idx].set_title(f'PDP and ICE for {feature_names[feature_idx]}')
        axes[feature_idx].legend(loc='lower right', frameon=False)

# Adjust layout and show plots
# plt.title('PDP and ICE for different chemical properties of the feasible solvents within the search domain')
# plt.subplots_adjust(wspace=0.5,hspace=0.5)
plt.tight_layout()
plt.savefig('pdp_ice_analysis_chemicalFeature_selection.png', dpi=400, pad_inches=0.03)
plt.savefig('pdp_ice_analysis_chemicalFeature_selection.pdf', dpi=400, pad_inches=0.03)
plt.show()

# from sklearn.inspection import PartialDependenceDisplay
#
# PartialDependenceDisplay.from_estimator(model, X, [0,1,2,3,4,5,6], kind='both')
# plt.tight_layout()
# plt.savefig('pdp_ice_analysis_2.png', dpi=400, pad_inches=0.03)
# plt.show()