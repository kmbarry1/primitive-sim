import argparse
from mpmath import mp
import primitive
from eth_abi import encode

mp.dps = 42

parser = argparse.ArgumentParser(description="mathematically check a primitive trade")
parser.add_argument("--x")
parser.add_argument("--y")
parser.add_argument("--strike")
parser.add_argument("--vol_bps")
parser.add_argument("--duration")
parser.add_argument("--ttm")
parser.add_argument("--xprime")
parser.add_argument("--yprime")

args = parser.parse_args()

x_start = mp.mpf(args.x) / 1e18
# print(x_start)
y_start = mp.mpf(args.y) / 1e18
# print(y_start)
strike = mp.mpf(args.strike) / 1e18
# print(strike)
sigma = mp.mpf(args.vol_bps) / 10000
# print(sigma)
tau = mp.mpf(args.ttm) / mp.mpf(args.duration)
# print(tau)
x_end = mp.mpf(args.xprime) / 1e18
# print(x_end)
y_end = mp.mpf(args.yprime) / 1e18
# print(y_end)

# I am lazy so I am hardcoding the pool fee. Protocol fee is zero.
fee_multiplier = mp.mpf(0.997)  # 30 basis points

if (x_end > x_start):
    # asset was sold
    dx = fee_multiplier * (x_end - x_start)
    y_highprec = primitive.get_y(x_start, y_start, strike, sigma, tau, dx)
#    print(y_end)
#    print("y_highprec: ", y_highprec)
    if y_highprec < 0:
        # can't go below zero
        y_highprec = 0
    newDependent = y_highprec
    ideal_output = y_start - y_highprec
    assert(ideal_output > 0)
    real_output = y_start - y_end
    err = (real_output - ideal_output) / ideal_output
    err = err * mp.sign(err)
#    print("err: ", err)
else:
    # asset was purchased
    assert(y_end > y_start)
    dy = fee_multiplier * (y_end - y_start)
    x_highprec = primitive.get_x(x_start, y_start, strike, sigma, tau, dy)
#    print(x_end)
#    print("x_highprec", x_highprec)
    if x_highprec < 0:
        # can't go below zero
        x_highprec = 0
    newDependent = x_highprec
    ideal_output = x_start - x_highprec
    assert(ideal_output > 0)
    real_output = x_start - x_end
    err = (real_output - ideal_output) / ideal_output
    err = err * mp.sign(err)
#    print("err: ", err)

newDependent = int(mp.nint(newDependent * 1e18))
#print(newDependent)
print("0x" + encode(['uint256'], [newDependent]).hex())
