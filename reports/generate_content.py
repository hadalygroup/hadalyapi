import datetime as dt
from reports.sections.General_description import general_description #done
from reports.sections.Performance import portfolio_performance, review_sp500 #done
from reports.sections.Events import previous_event, upcomming_event #done
#risk missing
from reports.sections.Risk import beta_evaluation, evaluate_risk
from reports.HTML import HTML
from typing import List

def generate_HTML(
        stock_list: List[str],
        n_stock: List[int],
        portfolio_value: int,
        important_stocks:str,
        portfolio_allocation: dict,
        portfolio: dict
        ):
    """"
    Generate the HTML code that will generate the whole report
    
    Calls:
        HTML-> Returns the unformatted string of the html code that needs to be filled
    """
    
    formated_HTML = HTML().format(date = dt.date.today().strftime("%Y-%m-%d"),
                                portfolio_value = portfolio_value,
                                important_stocks = important_stocks,
                                portfolio_overview = general_description(portfolio_allocation),
                                perfomance_vsSP500 = review_sp500(portfolio), #TODO
                                historical_performance = portfolio_performance(stock_list,n_stock),
                                beta_legend = beta_evaluation(), #TODO
                                risk_exposure = evaluate_risk(), #TODO
                                previous_events = previous_event(portfolio_allocation),
                                upcomming_event_ph = upcomming_event(portfolio_allocation)
                                )
    
    return formated_HTML