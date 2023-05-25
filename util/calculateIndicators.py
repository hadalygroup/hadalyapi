from talib import abstract
import pandas as pd
import numpy as np
import json

def calculateIndicator(stock_data, indicator):
    if isinstance(indicator, str):
        indicator_function = abstract.Function(indicator)
        value = indicator_function(stock_data)
    elif isinstance(indicator, dict):
        for key, value in indicator:
            ...
    elif isinstance(indicator, int):
        value = [indicator for i in range(len(stock_data['close']))]
        value = np.array(value)
    else:
        raise ValueError("Unsupported data type for indicator in calculateIndicator")
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

def getOptionnalParams(indicator_symbol):
    indicators_list = pd.read_csv("./util/indicators_params.csv")
    row = indicators_list.loc[indicators_list['indicator_name'] == indicator_symbol]
    indicators_params = row['indicator_default_para']
    indicators_params = indicators_params.values
    parameters_dict = json.loads(indicators_params.tolist()[0])
    default_param_dict = {}
    for param in parameters_dict:
        value = parameters_dict[param]
        if len(value) != 1:
            raise ValueError("Unsupported indicator: ", param, " is not supported")
        value = value[0]
        default_value = value["DEFAULT"]
        default_param_dict[param] = default_value
    return default_param_dict