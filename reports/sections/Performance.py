import datetime
from util.market_data import historical_data_gmd
from util.calculate_return import calculate_return
from util.sp500_performance import calculate_sp500_return as sp500
from util.ask_gpt import ask_GPT

def get_portfolio_return(stock_list, n_stocks):
    today = datetime.date.today()
    end_date = today.strftime("%Y-%m-%d")
    performance = {}
    for i in [7, 90, 365]:
        initial_value = 0
        final_value = 0
        start_date = today - datetime.timedelta(days=i)
        start_date = start_date.strftime("%Y-%m-%d")
        for i in range(len(stock_list)):
            price = historical_data_gmd(stock_list[i],start_date, end_date, "1d")
            initial_value += price[0] * n_stocks[i]
            final_value += price[-1] * n_stocks
        performance[i] = calculate_return(initial_value, final_value)
    return performance

def get_returns(stock_symbol, time):
    today = datetime.date.today()
    end_date = today.strftime("%Y-%m-%d")
    performance = []
    
    start_date = today - datetime.timedelta(days=time)
    start_date = start_date.strftime("%Y-%m-%d")
    data = historical_data_gmd(stock_symbol,start_date, end_date, "1d")
    starting_price = data['close'][0]
    final_price = data['close'][-1]
    performance = calculate_return(starting_price, final_price)
    return performance #[7d,3m,1y] list is returned

def review_stock_performance(stock_list, n_stocks):
    performances = get_portfolio_return(stock_list, n_stocks)
    performance_1w = performances[0]
    performance_3m = performances[1]
    performance_1y = performances[2]
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
    return ask_GPT(portfolio_performance_prompt)

def benchmark_comparison(stock_list, n_stocks):
    performances = get_portfolio_return(stock_list, n_stocks)
    performance_1y = performances[2]
    sp_500 = sp500(365)
    first_word = "Unfortunately"
    if performance_1y > sp_500:
        first_word = "Congratulations"
    benchmark_comparison_prompt = f"""You are a financial advisor.
    Write a short sentence to analyse weither my portfolio, which has had a {performance_1y}% return, has beaten the S&P500, which has had a {sp_500}% return in the past year. 
    Your first word has to be {first_word}.
    """
    return ask_GPT(benchmark_comparison_prompt)

def stock_performance(stock_list):
    stocks_performance = []
    for ticker in stock_list:
        stocks_performance.append(get_returns(ticker, 365))
    individual_stock_performance_prompt = f"""Act as a financial advisor.
    These are the returns that some stocks made in the past year: {stocks_performance}
    For comparison, {sp500(365)} was the performance of the S&P500 index.
    Which stocks have been the best performers?
    Your response will be something like "x and y were the best performers, while z was the worst performer"
    """
    return ask_GPT(individual_stock_performance_prompt)
    
def portfolio_performance(stock_list, n_stocks):
    performance_prompt = f"""
    resume the following paragraphs, without losing any information, in a single one under 200words.
    {review_stock_performance(stock_list, n_stocks)}
    {stock_performance(stock_list)}
    """
    return ask_GPT(performance_prompt)