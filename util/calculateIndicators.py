from talib import abstract
from datetime import date
import numpy as np

def calculateIndicator(stock_data, indicator):
    try:
        indicator_function = abstract.Function(indicator)
        value = indicator_function(stock_data)
    except Exception as e:
        print("Error in indicator calculation: ", e)
        value = [indicator for i in range(len(stock_data['close']))]
        value = np.array(value)
    return value

def calculateIndicators(stock_data, indicators):
    indicators_list = []
    for indicator in indicators:
        indicator_value = calculateIndicator(stock_data, indicator)
        if np.any(indicator_value == None):
            indicators_list.append(indicator)
            continue
        indicators_list.append(indicator_value.tolist())
    return indicators_list