import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.model_selection import train_test_split
import time # for tic-toc
from sklearn.preprocessing import OneHotEncoder

import pandas as pd

# Load the Excel file
file_path = 'suzuki_experiment_index_formatted.xlsx'
sheet_name = 'ohe'
data = pd.read_excel(file_path, sheet_name=sheet_name)

X = data.iloc[:, 1:-1].values
y = data.iloc[:, -1].values

from pyparc.parc import PARC

np.random.seed(0)  # for reproducibility
cpu_time = {}
test_size = 0.2

K = 10
separation = 'Softmax'
# separation='Voronoi'
sigma = 1
alpha = 1.0e-4
beta = 1.0e-3
softmax_maxiter = 100000
maxiter = 15


categorical = False  # whether the output is categorical

# One-hot encode the categorical variable
encoder = OneHotEncoder(sparse_output=False, categories='auto')
X_categorical_encoded = encoder.fit_transform(X.ravel().reshape(-1, 5))

X_train, X_test, Y_train, Y_test = train_test_split(X_categorical_encoded, y, test_size=test_size, shuffle=True)

tic = time.process_time()
predictor = PARC(K=K, alpha=alpha, sigma=sigma, separation=separation, maxiter=maxiter,
                 cost_tol=1e-4, min_number=10, fit_on_partition=True,
                 beta=beta, verbose=0)

# Y_hat, delta_hat = predictor.predict(X_test) # predict targets

predictor.fit(X_train, Y_train, categorical, weights=np.ones(1))
toc = time.process_time()
cpu_time["PWAS"] = toc - tic

print("Model fitting time required (%f)", (cpu_time["PWAS"]))

score_train = predictor.score(X_train, Y_train)  # compute R2 score on training data
score_test = predictor.score(X_test, Y_test)  # compute R2 score on test data

print("\nResults:\n")
print("Training data: %6.2f %%" % (score_train[0] * 100))
print("Test data:     %6.2f %%" % (score_test[0] * 100))
print("--------------------\n")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, DotProduct, WhiteKernel
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder

# Use the same training samples as for PWAS

tune_gp = False

if tune_gp:
    # Define kernels with tunable parameters
    kernels = [
        RBF(),  # Length scale will be tuned
        Matern(),  # Length scale and nu will be tuned
        DotProduct() + WhiteKernel()  # Noise level of WhiteKernel will be tuned
    ]

    # Define parameter grid for each kernel
    param_grid = [
        {'kernel': [RBF()], 'kernel__length_scale': [0.1, 1.0, 10.0]},
        {'kernel': [Matern()], 'kernel__length_scale': [0.1, 1.0, 10.0], 'kernel__nu': [0.5, 1.5, 2.5]},
        {'kernel': [DotProduct() + WhiteKernel()], 'kernel__k2__noise_level': [0.1, 1.0, 10.0]}
    ]
else:
    kernels = [
        RBF(length_scale=1.0),
        Matern(length_scale=1.0, nu=1.5),
        DotProduct() + WhiteKernel(noise_level=1)
    ]

# Train a Gaussian Process model with GridSearchCV for each kernel
results = {}
for i, kernel in enumerate(kernels):
    if tune_gp:
        tic = time.process_time()
        gp = GaussianProcessRegressor()
        grid_search = GridSearchCV(gp, param_grid[i], cv=3, n_jobs=-1, scoring='r2')
        grid_search.fit(X_train, Y_train)
        toc = time.process_time()

        # Best model
        best_gp = grid_search.best_estimator_
        cpu_time[str(best_gp.kernel)] = toc - tic

        # Scoring
        train_score = best_gp.score(X_train, Y_train)
        test_score = best_gp.score(X_test, Y_test)
    else:
        tic = time.process_time()
        kernel_name = str(kernel)  # Convert the kernel object to a string
        gp = GaussianProcessRegressor(kernel=kernel)
        gp.fit(X_train, Y_train)
        toc = time.process_time()
        cpu_time[str(kernel)] = toc - tic

        # Scoring
        train_score = gp.score(X_train, Y_train)
        test_score = gp.score(X_test, Y_test)

    if tune_gp:
        # Store results
        results[str(best_gp.kernel)] = {
            "train_score": train_score,
            "test_score": test_score,
            "best_params": grid_search.best_params_,
            "best_gp": best_gp
        }
    else:
        results[str(kernel)] = {
            "train_score": train_score,
            "test_score": test_score,
            "best_gp": gp
        }

print("\nResults:\n")
for i, (kernel_name, res) in enumerate(results.items()):
    print(f"Training data {kernel_name}: %6.2f %%" % (res['train_score'] * 100))
    print(f"Test data {kernel_name}:     %6.2f %%" % (res['test_score'] * 100))
    print("--------------------\n")

print(cpu_time)