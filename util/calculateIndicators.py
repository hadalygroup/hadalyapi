from talib import abstract
import pandas as pd
import numpy as np
import json

def calculateIndicator(stock_data, indicator):
    if isinstance(indicator, str):
        indicator_function = abstract.Function(indicator)
        value = indicator_function(stock_data)
    elif isinstance(indicator, dict):
        try: 
            indicator_symbol = getDictKey(indicator)
            if indicator_symbol.isdigit():
                return intIndicator(indicator_symbol, len(stock_data['close']))
            optional_params = getOptionnalParams(indicator)
            indicator_function = abstract.Function(indicator_symbol)
        except ValueError:
            raise ValueError("Unsopported indicator : ", indicator)
            print("Indicator will not be calculated and will be set to 0")
            return 0
        #indicator is a dict that has the following form:
        #{'RSI': {'time': '0', 'source': 'close', 'timeperiod': '14'}}
        #we use the following for loop to unpack the indicator_symbol and its params even though we do not iterate over it multiple times
        params = indicator[indicator_symbol]
        for param, argument in params.items():
            optional_params[param] = argument
        
        params = convert(optional_params)
        value = indicator_function(stock_data, **params)
        if "time" in indicator[indicator_symbol]:
            time_offset = int(indicator[indicator_symbol]["time"])
            value = offset_list(value,time_offset)

    else:
        raise ValueError("Unsupported data type for indicator in calculateIndicator")
    return value

def intIndicator(intAsString, length):
    value = [int(intAsString) for i in range(length)]
    value = np.array(value)
    return value

def getDictKey(dictionnary):
    for key in dictionnary:
        dictionnary=key
    return dictionnary

def convert(parameters):
    string_conversion = ""
    for key, value in parameters.items():
        if not isinstance(value, int):
            if value.isdigit():
                value = int(value)
        parameters[key] = value
    return parameters

def calculateIndicators(stocks_data,indicators):
    indicators_list = []
    for indicator in indicators:
        indicator_value = calculateIndicator(stocks_data,indicator)
        if np.any(indicator_value == None):
            indicators_list.append(indicator)
            continue
        
        if not isinstance(indicator_value, np.ndarray):
            for i in len(range(indicator_value)):
                indicator_value[i] = indicator_value[i].tolist()
        else:
            indicator_value = indicator_value.tolist()
        indicators_list.append(indicator_value)
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

def offset_list(data,time_offset:int):
    if time_offset == 0:
        return data
    nan_offset = [np.nan] * time_offset
    if isinstance(data, np.ndarray):
        data = data.tolist()
    data = nan_offset + data
    data = data[:-time_offset]
    data = np.array(data)
    return data
