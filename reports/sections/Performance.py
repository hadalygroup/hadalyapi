import datetime
from util.market_data import historical_data_gmd
from util.calculate_return import calculate_return
from util.sp500_performance import calculate_sp500_return as sp500
from util.ask_gpt import ask_GPT
from typing import List

def get_portfolio_return(portfolio: dict) -> float:
    """
    Calculate the performance of the portfolio in the last 7, 90 and 365 days
    Input:
        portfolio -> dict of the portfolio where the keys are the stock tickers and the values are the number of stocks owned

    Output:
        performance[7] -> performance of the portfolio in % in the last 7days
        performance[90] -> performance of the portfolio in % in the last 90days
        performance[365] -> performance of the portfolio in % in the last 365days

    """

    today = datetime.date.today()
    end_date = today.strftime("%Y-%m-%d")
    performance = {}
    for i in [7, 90, 365]:
        initial_value = 0
        final_value = 0
        start_date = today - datetime.timedelta(days=i)
        start_date = start_date.strftime("%Y-%m-%d")
        for ticker, amount in portfolio.items():
            price = historical_data_gmd(ticker,start_date, end_date, "1d")
            initial_value += price["close"][0] * amount
            final_value += price["close"][-1] * amount
        performance[i] = calculate_return(initial_value, final_value)
    return performance[7], performance[90], performance[365]

def get_returns(stock_symbol: str, time: int) -> float:
    """
    Calculate performance of one stock in the last (time) days
    
    Input:
        stock_symbol
        time: Number of how much days to look in the past
    Output:
        performance
    """
    today = datetime.date.today()
    end_date = today.strftime("%Y-%m-%d")
    performance = []
    
    start_date = today - datetime.timedelta(days=time)
    start_date = start_date.strftime("%Y-%m-%d")
    data = historical_data_gmd(stock_symbol,start_date, end_date, "1d")
    starting_price = data['close'][0]
    final_price = data['close'][-1]
    performance = calculate_return(starting_price, final_price)
    return performance

def review_portfolio_performance(portfolio) -> str:
    """
    Asking GPT to review the performance of the portfolio
    Input:
        portfolio -> dict of the portfolio where the keys are the stock tickers and the values are the number of stocks owned
    Output:
        response -> GPT's review
    """

    performance_1w, performance_3m, performance_1y = get_portfolio_return(portfolio)
 
    portfolio_performance_prompt = f"""You are a financial advisor.
    Here is the performance of a portfolio in the last year, 3months and 1w respectively:
        -in the last year : {performance_1y}
        -in the last 3months : {performance_3m}
        -in the last week : {performance_1w}
    What can conclusions can be drawn from these metrics? How volatile and secure is the portfolio?
    What changes can you suggest for an investor with high risk tolerance?
    What changes can you suggest for an investor with low risk tolerance?
    Be concise and explain everything you advance, your first sentence will start with "The volatility of this portfolio may be considered [....], due to [...]"
    """
    response = ask_GPT(portfolio_performance_prompt)
    return response

def review_sp500(portfolio):
    """
    Compare portfolio and SP500

    Input:
        portfolio -> dict of the portfolio where the keys are the stock tickers and the values are the number of stocks owned
    Output:
        benchmark_interpretation -> String to congratulate (or not) the user for beating (or not) the benchmark
    """
    _,_, performance_1y = get_portfolio_return(portfolio)
    sp_500 = sp500(365)
    difference = performance_1y - sp_500
    difference = round(difference, 3)
    benchmark_interpretation = f"Unfortunately, your portfolio did not beat the S&P500 by {difference}%"
    if difference>0:
        benchmark_interpretation = f"Congratulations, your portfolio has beaten the S&P500 by {difference}%"
    return benchmark_interpretation

def review_stock_performance(stock_list):
    """
    Reviewing the stocks individually and comparing each to the SP500

    Input:
        stock_list -> List of the stock tickers
    Output:
        response -> GPT's general review of all the stocks
    """
    stocks_performance = []
    for ticker in stock_list:
        stocks_performance.append(get_returns(ticker, 365))
    individual_stock_performance_prompt = f"""Act as a financial advisor.
    These are the returns that some stocks made in the past year: {stocks_performance}
    For comparison, {sp500(365)} was the performance of the S&P500 index.
    Which stocks have been the best performers?
    Your response will be something like "x and y were the best performers, while z was the worst performer"
    """
    response = ask_GPT(individual_stock_performance_prompt)
    return response
    
def portfolio_performance(portfolio):
    """
    Resume all of the info in one paragraph (generate the whole portfolio performance section of the report)

    Input:
        portfolio -> dict of the portfolio where the keys are the stock tickers and the values are the number of stocks owned
    Output:
        response -> GPT's general review of all the stocks
    
    """
    stock_list = list(portfolio.keys())
    stock_performance_review = review_stock_performance(stock_list)
    portfolio_performance_review = review_portfolio_performance(portfolio)
    performance_prompt = f"""
    resume the following paragraphs, without losing any information, in a single one under 200words.
    {portfolio_performance_review}
    {stock_performance_review}
    """
    response = ask_GPT(performance_prompt)
    return response