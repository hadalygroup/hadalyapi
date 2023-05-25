from talib import abstract
import pandas as pd
import numpy as np
import json

def calculateIndicator(stock_data, indicator):
    if isinstance(indicator, str):
        indicator_function = abstract.Function(indicator)
        value = indicator_function(stock_data)
    elif isinstance(indicator, int):
        value = [indicator for i in range(len(stock_data['close']))]
        value = np.array(value)
    elif isinstance(indicator, dict):
        try: 
            optional_params = getOptionnalParams(indicator)
            indicator_symbol = getDictKey(indicator)
        except ValueError:
            raise ValueError("Unsopported indicator : ", indicator)
            print("Indicator will not be calculated and will be set to 0")
            return 0
        
        if "time" in indicator[indicator_symbol]:
            ... #TODO: call calculate indicator with for each time 
            return ...
            # stock_data_index = stock_data_index - indicator["time"]
            # stock_data = stocks_data[stock_data_index]
        
        #indicator is a dict that has the following form:
        #{'RSI': {'time': '0', 'source': 'close', 'timeperiod': '14'}}
        #we use the following for loop to unpack the indicator_symbol and its params even though we do not iterate over it multiple times
        params = indicator[indicator_symbol]
        for param, argument in params.items():
            optional_params[param] = argument
        
        params = convert(optional_params) 
        indicator_function = abstract.Function(indicator_symbol)
        value = indicator_function(stock_data, **params)

    else:
        raise ValueError("Unsupported data type for indicator in calculateIndicator")
    return value

def getDictKey(dictionnary):
    for key in dictionnary:
        dictionnary=key
    return dictionnary

def convert(parameters):
    string_conversion = ""
    for key, value in parameters.items():
        if value.isdigit():
            value = int(value)
        parameters[key] = value
    return parameters

def calculateIndicators(stocks_data,indicators):
    indicators_list = []
    for indicator_index in indicators:
        indicator = indicators[indicator_index]
        indicator_value = calculateIndicator(stocks_data,indicators)
        if np.any(indicator_value == None):
            indicators_list.append(indicator)
            continue
        indicators_list.append(indicator_value.tolist())
    return indicators_list

def getOptionnalParams(indicator_symbol):
    indicator_symbol = getDictKey(indicator_symbol)
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
