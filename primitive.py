from mpmath import mp
from scipy import special
import numpy as np

SECONDS_PER_YEAR = 31556953

# inverse CDF
def cdfinv(x):
    return mp.sqrt(2) * mp.erfinv(2*x - 1)

def cdfinv_scipy(x):
    return np.sqrt(2) * special.erfinv(2*x - 1)

# this gives good results (with enough precision)
def sanity_check(x):
    return mp.ncdf(cdfinv(x))

def invariant(x, y, strike, sigma, tau):
    # mp.mpf(*) wrapping done just in case args aren't already mpfs
    yTerm = cdfinv(y / mp.mpf(strike))
    xTerm = cdfinv(mp.mpf(1) - x)
    sigmaSqrtTau = sigma * mp.sqrt(tau / mp.mpf(SECONDS_PER_YEAR))
    print(yTerm)
    print(xTerm)
    print(sigmaSqrtTau)
    return yTerm - xTerm + sigmaSqrtTau

def invariant_scipy(x, y, strike, sigma, tau):
    yTerm = cdfinv_scipy(np.float64(y) / strike)
    xTerm = cdfinv_scipy(np.float64(1) - x)
    sigmaSqrtTau = sigma * np.sqrt(tau / np.float64(SECONDS_PER_YEAR))
    print(yTerm)
    print(xTerm)
    print(sigmaSqrtTau)
    return yTerm - xTerm + sigmaSqrtTau
