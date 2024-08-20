from pwasopt.main_pwas import PWAS
from pwasopt.main_pwasp import PWASp
from pwasopt.pref_fun1 import PWASp_fun1
from pwasopt.pref_fun import PWASp_fun

from numpy import array, zeros, ones
import numpy as np
import math
import sys


# ==========================================================================================================================================================
# the following rosenbrock, six-hump camel, and beal functions are used for comparison
# Taken from: https://github.com/rubinxin/CoCaBO_code/blob/master/testFunctions/syntheticFunctions.py
# =============================================================================
# Rosenbrock Function (f_min = 0)
# https://www.sfu.ca/~ssurjano/rosen.html
# =============================================================================
def myrosenbrock(X):
    X = np.asarray(X)
    X = X.reshape((-1, 2))
    if len(X.shape) == 1:  # one observation
        x1 = X[0]
        x2 = X[1]
    else:  # multiple observations
        x1 = X[:, 0]
        x2 = X[:, 1]
    fx = 100 * (x2 - x1 ** 2) ** 2 + (x1 - 1) ** 2
    return fx.reshape(-1, 1) / 300


# =============================================================================
#  Six-hump Camel Function (f_min = - 1.0316 )
#  https://www.sfu.ca/~ssurjano/camel6.html
# =============================================================================
def mysixhumpcamp(X):
    X = np.asarray(X)
    X = np.reshape(X, (-1, 2))
    if len(X.shape) == 1:
        x1 = X[0]
        x2 = X[1]
    else:
        x1 = X[:, 0]
        x2 = X[:, 1]
    term1 = (4 - 2.1 * x1 ** 2 + (x1 ** 4) / 3) * x1 ** 2
    term2 = x1 * x2
    term3 = (-4 + 4 * x2 ** 2) * x2 ** 2
    fval = term1 + term2 + term3
    return fval.reshape(-1, 1) / 10


# =============================================================================
# Beale function (f_min = 0)
# https://www.sfu.ca/~ssurjano/beale.html
# =============================================================================
def mybeale(X):
    X = np.asarray(X) / 2
    X = X.reshape((-1, 2))
    if len(X.shape) == 1:
        x1 = X[0] * 2
        x2 = X[1] * 2
    else:
        x1 = X[:, 0] * 2
        x2 = X[:, 1] * 2
    fval = (1.5 - x1 + x1 * x2) ** 2 + (2.25 - x1 + x1 * x2 ** 2) ** 2 + (
            2.625 - x1 + x1 * x2 ** 3) ** 2
    return fval.reshape(-1, 1) / 50



if benchmark == 'Func-2C':
    nc = 2
    nint = 0
    nd = 2
    X_d = [3, 3]
    lb = array([-1, -1, 0, 0])
    ub = array([1, 1, 2, 2])


    def fun(x):
        xc = x[:nc]
        xd = np.around(x[nc:])

        # xc = xc * 2

        assert len(xd) == 2
        ht1 = xd[0]
        ht2 = xd[1]

        if ht1 == 0:  # rosenbrock
            f = myrosenbrock(xc)
        elif ht1 == 1:  # six hump
            f = mysixhumpcamp(xc)
        elif ht1 == 2:  # beale
            f = mybeale(xc)

        if ht2 == 0:  # rosenbrock
            f = f + myrosenbrock(xc)
        elif ht2 == 1:  # six hump
            f = f + mysixhumpcamp(xc)
        else:
            f = f + mybeale(xc)

        y = f + 1e-6 * np.random.rand(f.shape[0], f.shape[1])
        return y[0][0]


    fopt0 = -0.20632
    xopt0 = array([[0.0898, -0.0898, 1, 1], [-0.7126, 0.7126, 1, 1]])



elif benchmark == 'Func-3C':
    nc = 2
    nint = 0
    nd = 3
    X_d = [3, 3, 3]
    lb = array([-1, -1, 0, 0, 0])
    ub = array([1, 1, 2, 2, 2])


    def fun(x):
        xc = x[:nc]
        xd = np.around(x[nc:])

        xc = np.atleast_2d(xc)
        assert len(xd) == 3
        ht1 = xd[0]
        ht2 = xd[1]
        ht3 = xd[2]

        # xc = xc * 2
        if ht1 == 0:  # rosenbrock
            f = myrosenbrock(xc)
        elif ht1 == 1:  # six hump
            f = mysixhumpcamp(xc)
        elif ht1 == 2:  # beale
            f = mybeale(xc)

        if ht2 == 0:  # rosenbrock
            f = f + myrosenbrock(xc)
        elif ht2 == 1:  # six hump
            f = f + mysixhumpcamp(xc)
        else:
            f = f + mybeale(xc)

        if ht3 == 0:  # rosenbrock
            f = f + 5 * mysixhumpcamp(xc)
        elif ht3 == 1:  # six hump
            f = f + 2 * myrosenbrock(xc)
        else:
            f = f + ht3 * mybeale(xc)

        y = f + 1e-6 * np.random.rand(f.shape[0], f.shape[1])

        return y[0][0]


    fopt0 = -0.72214
    xopt0 = array([[0.0898, -0.0898, 1, 1, 0], [-0.7126, 0.7126, 1, 1, 0]])

    isLin_eqConstrained = False
    isLin_ineqConstrained = False

    maxevals = 100
    n_initil = 20

elif benchmark == 'Ackley-cC':
    nc = 1
    nint = 0
    # nd = 2  # Ackley-2C
    # nd = 3  # Ackley-3C
    # nd = 4  # Ackley-4C
    nd = 5  # Ackley-5C
    X_d = [17] * nd
    lb_cont = -ones((1))
    ub_cont = ones((1))
    lb_binary = zeros((nd))
    ub_binary = 16 * ones((nd))
    lb = np.hstack((lb_cont, lb_binary))
    ub = np.hstack((ub_cont, ub_binary))


    def fun(x):
        xc = x[:nc]
        xd = np.around(x[nc:])
        n = nc + nd

        a = 20
        b = 0.2
        c = 2 * np.pi
        s1 = 0
        s2 = 0

        x_ak = zeros((nc + nd, 1))
        x_ak[:nc, 0] = xc

        for i in range(nd):
            x_ak[nc + i, 0] = -1 + 0.125 * xd[i]

        for i in range(n):
            s1 += x_ak[i, 0] ** 2
            s2 += math.cos(c * x_ak[i, 0])

        f = -a * math.exp(-b * (1 / n * s1) ** (1 / 2)) - math.exp(1 / n * s2) + a + math.exp(1)

        return f


    isLin_eqConstrained = False
    isLin_ineqConstrained = False

    xopt0 = array([0, 8, 8, 8, 8, 8])
    fopt0 = 0

    maxevals = 100

    n_initil = 20
