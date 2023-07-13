from util.ask_gpt import ask_GPT

def beta_evaluation(beta: float):
    """
    Interpret the beta value of the portfolio

    Input:
        beta: the beta value of the portfolio
    """
    beta = abs(beta)
    if beta >= 2:
        beta_interpretation = "A portfolio exhibiting a calculated absolute beta exceeding 2 is characterized by pronounced volatility."
    elif beta >= 1.5:
        beta_interpretation = "An absolute beta value superior to 1.5 in a portfolio suggests that the portfolio is expected to be 50% more volatile than the overall market."
    elif beta >=1:
        beta_interpretation = "An absolute beta value of 1 indicates that the portfolio is expected to move in line with the overall market."
    elif beta >= 0.5:
        beta_interpretation = "A portfolio having an absolute beta greater than 0.5 but less than one suggests that the asset or portfolio is less volatile than the market but still demonstrates some sensitivity to market movements"
    elif beta >= 0:
        beta_interpretation = "A portfolio with an absolute beta value less than 0.5 carries the risk of underperformance during market upswings, limited exposure to market gains, and potential losses during market downturns."
    return beta_interpretation

def evaluate_risk(portfolio_beta: float, betas: dict):
    """
    Discuss the overall risk level of your portfolio. 
    You can use measures like beta to quantify risk. (news, economical events, recent acquisition, alarming numbers, result)
    Discuss your portfolio's exposure to the overall market. If the market were to go up or down, how would your portfolio be affected?

    Inputs:
        portfolio_beta: The overall beta value of the portfolio
        betas: Dictionnary of the stocks and their corresponding betas
    """
    risk_exposure_prompt = f"""Act as a financial advisor.
    Here is a list of stocks and their corresponding betas: {betas}.
    Also, the whole portfolio has a beta of {portfolio_beta}.
    Evaluate the market risk of the portfolio, what are the consequences? Are there solutions to increase revenue?
    Explain and evaluate the systematic risk.
    What are the actions a holder with strong risk tolerance wanting short term gains should do?
    What are the actions a holder with little risk tolerance should do?
    Keep it concise, I will write your first sentences: "Beta is a measure of a stock's volatility in relation to the market. Based on your stocks and their betas, your portfolio has a beta of {portfolio_beta}, [...]"
    """
    return ask_GPT(risk_exposure_prompt)