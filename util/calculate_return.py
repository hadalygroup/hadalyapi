def calculate_return(starting_price, final_price):
    stock_return = (final_price - starting_price) / starting_price * 100
    return round(stock_return, 3)