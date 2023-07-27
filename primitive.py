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
#    print(yTerm)
#    print(xTerm)
#    print(sigmaSqrtTau)
    return yTerm - xTerm + sigmaSqrtTau

# "implied" y value given other params (subtracted from "real" y value in original invariant formula)
def implied_y(x, strike, sigma, tau):
    tau = tau / mp.mpf(SECONDS_PER_YEAR)
    return strike * mp.ncdf(cdfinv(mp.mpf(1) - x) - sigma * mp.sqrt(tau))

def invariant_original(x, y, strike, sigma, tau):
    return y - implied_y(x, strike, sigma, tau)

def spot_price_volatile_asset(x, y, strike, sigma, tau):
    tau = tau / mp.mpf(SECONDS_PER_YEAR)
    price = strike
    price *= mp.exp(cdfinv(mp.mpf(1) - x) * sigma * tau)
    price *= mp.exp(mp.mpf(-0.5) * mp.power(sigma, 2) * tau)
    return price

# will return a negative number as dx postive => dy negative
def get_dy(x, strike, sigma, tau, dx):
    assert(dx >= 0)
    return implied_y(x + dx, strike, sigma, tau) - implied_y(x, strike, sigma, tau)

def get_y(x, y, strike, sigma, tau, dx):
    assert(dx >= 0)
    return y + get_dy(x, y, strike, sigma, tau, dx)

def get_x(x, y, strike, sigma, tau, dy):
    assert(dy >= 0)

    # call other functions PRIOR to scaling tau
    k = invariant_original(x, y, strike, sigma, tau)
    tau = tau / mp.mpf(SECONDS_PER_YEAR)
    return 1 - mp.ncdf(cdfinv((mp.mpf(y) + dy - k) / strike) + sigma * mp.sqrt(tau))

# will return a negative number as dy postive => dx negative
def get_dx(x, y, strike, sigma, tau, dy):
    assert(dy >= 0)
    return get_x(x, y, strike, sigma, tau, dy) - x
