import numpy as np

def get_value_at_time(t, calcul):
    t = int(t)
    ad = [np.NaN for k in range(t)]
    real = ad + list(calcul[0:len(calcul) - t])
    return real