import numpy as np 

# Utility functions for sampling distributions.
def sample_categorical(rng, params):
    pvals = np.array(params)
    pvals = pvals / np.sum(pvals)
    draw_array = rng.multinomial(n=1, pvals=pvals)
    return np.argmax(draw_array)

def sample_normal(rng, params):
    return rng.normal(loc=params[0], scale=params[1])

def clamp_min_max(x, min, max):
    if x <= min: return min
    if x >= max: return max
    return x