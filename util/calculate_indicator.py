import talib
import numpy as np
from util.get_value_at_time import get_value_at_time

def calculate_indicators(inputs, ind_to_calculate: str, ADOSC_fastperiod = 3, ADOSC_slowperiod = 10):
    # ind=str(list(ind_to_calculate.keys())[0])
    #i=ind_to_calculate[ind]
    dic={}

    indicator_function = getattr(talib, ind_to_calculate)
    H = np.array(inputs['high'])
    O = np.array(inputs['open'])
    L = np.array(inputs['low'])
    C = np.array(inputs['close'])
    real = indicator_function(O,H,L,C)
    #real = get_value_at_time(i['time'],real)
    return real