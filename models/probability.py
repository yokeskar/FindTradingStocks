import numpy as np
from scipy.stats import norm

def implied_move(current_price, iv_annual, days):
    t = days / 252
    sigma = iv_annual / 100
    return current_price * (np.exp(sigma * np.sqrt(t)) - 1)

def probability_above(current_price, strike, iv_annual, days):
    t = days / 252
    sigma = iv_annual / 100
    mu = -0.5 * sigma**2

    d = (np.log(current_price / strike) + (mu + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
    return 1 - norm.cdf(d)
