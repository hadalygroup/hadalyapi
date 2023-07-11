import datetime as dt
from reports.sections.General_description.General_description import general_description 
from reports.sections.Performance import portfolio_performance, review_sp500 
from reports.sections.Events import previous_event, upcomming_event

from reports.sections.Risk.Risk import beta_evaluation, evaluate_risk
from reports.HTML import HTML
from typing import List, Tuple

def generate_HTML(
        portfolio: dict,
        portfolio_value: int,
        important_stocks: List[Tuple],
        portfolio_allocation: dict,
        portfolio_beta: float,
        betas: dict
        ):
    """"
    Generate the HTML code that will generate the whole report
    
    Calls:
        HTML-> Returns the unformatted string of the html code that needs to be filled
    """
    html = HTML()

    today_date = dt.date.today().strftime("%Y-%m-%d")

    general_description_paragraph = general_description(portfolio_allocation)
    
    benchmark_result = review_sp500(portfolio)

    historical_performance_paragraph = portfolio_performance(portfolio)

    beta_interpretation =  beta_evaluation(portfolio_beta)

    risk_exposure_paragraph = evaluate_risk(portfolio_beta, betas)

    past_events = previous_event(portfolio_allocation)

    next_events = upcomming_event(portfolio_allocation)

    formated_HTML = html.format(date = today_date,
                                portfolio_value = portfolio_value, #done
                                important_stocks = important_stocks, #done
                                portfolio_overview = general_description_paragraph, #done
                                performance_vsSP500 = benchmark_result, 
                                historical_performance = historical_performance_paragraph, #done
                                beta_legend = beta_interpretation, #done
                                risk_exposure = risk_exposure_paragraph, #done
                                previous_events = past_events, #done
                                upcomming_events = next_events #done
                                )
    print("here2")
    return formated_HTML