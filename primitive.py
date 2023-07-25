from mpmath import mp

# inverse CDF
def cdfinv(x):
    return mp.sqrt(2) * mp.erfinv(2*x - 1)

def invariant(x, y, strike, sigma, tau):
    yTerm = cdfinv(y / mp.mpf(strike))  # casting just in case args weren't already mpfs
    xTerm = cdfinv(mp.mpf(1) - x)  # casting for same reason as above
    sigmaSqrtTau = sigma * mp.sqrt(tau)
    return yTerm - xTerm + sigmaSqrtTau
