from util.ask_gpt import ask_GPT

def overview(portfolio_allocation: dict) -> str:
    """
    Briefly describe the composition of your portfolio, including the names and sectors of 
    the stocks you hold (AAPL - Technology, TSLA - Consumer Cyclical, MSFT - Technology).


    Input:
        portfolio_allocation: dictionnary where the keys are the tickers and the values are the percentage(%) each is occupying in the portfolio
    """

    overview_prompt = f"""Act as a banker.
    Describe the composition of a portfolio holding these stocks: {portfolio_allocation.keys()}, but dont repeat this information.
    Here is the allocation in % of the portfolio {portfolio_allocation}.
    Include the name, the industrial sectors of each compagnies and naming the sectors the portfolio is the most exposed to.
    Your response should be around be concise and make sure not to repeat yourself. Your first sentence will be "Your portfolio is composed of stocks from compagnies operating in [...]"
    """
    return ask_GPT(overview_prompt)

def review_investment_strategy(portfolio_allocation: dict) -> str:
    """
    State the current type of portfolio:
    Is it  aiming for growth, income, or a balance of the two? 
    Is it for the long term or short term?


    Input:
        portfolio_allocation: dictionnary where the keys are the tickers and the values are the percentage(%) each is occupying in the portfolio
    
    """

    investment_strategy_prompt = f"""Act as a financial advisor.
    What type of portfolio is {list(portfolio_allocation.keys())}. The allocation is {portfolio_allocation} in percentage.
    Is it aiming for growth or income?
    Is it aiming for long or short term?
    Is it well diversified accross different sectors?
    Base your analysis on two types of investors: one with high and the other with low risk tolerance.
    Be concise and precise in your answer, explain everything you advance. 
    Your first sentence will be "Your portfolio appears to aim for [...]"
    """
    return ask_GPT(investment_strategy_prompt)

def review_allocation(portfolio_allocation: dict) -> str:
    """
    Discuss the allocation of your portfolio. 
    How much of your portfolio is invested in each stock? 
    Are you diversified across different sectors?

    Input:
        portfolio_allocation: dictionnary where the keys are the tickers and the values are the percentage(%) each is occupying in the portfolio
    
    """

    allocation_prompt = f"""You are a financial advisor.
    Discuss the relevant sectors that might be interesting to add to diversify a portfolio that already owns these stock {portfolio_allocation.keys()}.
    Be concise and explaining everything you advance, your first sentence will be "Based on the stocks you already own, we recommand you to add [the sectors] because [...]"
    """
    return ask_GPT(allocation_prompt)

def general_description(portfolio_allocation: dict) -> str:
    """
    Reviewing the whole overview section, linking paragraphs together and make sure they all fit together

    Input:
        portfolio_allocation: dictionnary where the keys are the tickers and the values are the percentage(%) each is occupying in the portfolio
    
    """

    overview_paragraph = overview(portfolio_allocation)
    investment_strategy_paragraph = review_investment_strategy(portfolio_allocation)
    allocation_paragraph = review_allocation(portfolio_allocation)

    general_description_prompt = f"""
    resume those paragraphs, without losing any information, in a single paragraph be concise and try to fit all information in under 200words.
    {overview_paragraph}
    {investment_strategy_paragraph}
    {allocation_paragraph}
    """
    return ask_GPT(general_description_prompt)