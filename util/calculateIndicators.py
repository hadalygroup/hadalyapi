from talib import abstract
import numpy as np

def calculateIndicator(stock_data, indicator):
    try:
        indicator_function = abstract.Function(indicator)
        value = indicator_function(stock_data)
    except Exception as e:
        print("Error in indicator calculation: ", e)
        value = np.array([])
    return value

def calculateIndicators(stock_data, indicators):
    indicators_list = []
    for indicator in indicators:
        indicator_value = calculateIndicator(stock_data, indicator)
        indicators_list.append(indicator_value.tolist())
    return indicators_list