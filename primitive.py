from mpmath import mp

SECONDS_PER_YEAR = 31556953

# inverse CDF
def cdfinv(x):
    return mp.sqrt(2) * mp.erfinv(2*x - 1)

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
