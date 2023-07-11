def important_stocks(portfolio_allocation):
    sorted_portfolio = sorted(portfolio_allocation.items(), key=lambda x:x[1], reverse=True)
    important_stocks = ""
    for index, item in enumerate(sorted_portfolio[:3]):
        stock, value = item
        important_stocks += f"{stock} at {value}%"
        if index != 2:
            important_stocks += ", "
    return important_stocks