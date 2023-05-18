from talib import abstract

def calculateIndicator(stock_data, indicator):
    indicator_function = abstract.Function(indicator)
    value = indicator_function(stock_data)
    return value

def calculateIndicators(stock_data, indicators):
    indicators_list = []
    print("ici")
    for indicator in indicators:
        indicator_value = calculateIndicator(stock_data, indicator)
        indicators_list.append(indicator_value.tolist())
    return indicators_list