import datetime
from util.events import get_economic_calendar
from util.ask_gpt import ask_GPT
import ast
import pandas as pd
from typing import List


def get_events(timeframe: int) -> pd.DataFrame:
    """
    Returns a list of all the economic events in the past week

    Input:
        timeframe: Number of days in the future (negative if want to look in the past)

    Output:
        events: dataframe of the events containing the following columns: 
            Time (ET)   Country   Event   Actual   Concensus   Previous   Date
    """
    today = datetime.date.today()
    other_date = today + datetime.timedelta(days=timeframe)
    today = today.strftime('%Y-%m-%d')
    other_date = other_date.strftime('%Y-%m-%d')
    
    if timeframe > 0:
        events = get_economic_calendar(start_date=today, end_date=other_date, countries= ['Canada', 'United States'])
    else:
        events = get_economic_calendar(start_date=other_date, end_date=today, countries= ['Canada', 'United States'])
    
    return events


def review_events(events: pd.DataFrame, portfolio_allocation: dict) -> List[str]:
    """
    Asking GPT to review the all the events and return a list of the most important ones for the portfolio

    Input: 
        events: dataframe of all the events in the given timeframe
        portfolio_allocation: Dictionnary where the keys are the stock tickers and the values are the percentage of each one in this portfolio
    Output:
        events -> Lists[events(strings)]
    """
    events_list = events["Event"].tolist()

    past_events_prompt = f"""{events_list}
    From these events return a python array(list) of the 3 most important ones for this portfolio: {list(portfolio_allocation.keys())}
    """
    response = ask_GPT(past_events_prompt)
    try:
        events = ast.literal_eval(response)
    except Exception as e:
        print("Error as occured in review_past_events: ", e)
        return None
    return events

def describe_events(events: pd.DataFrame, important_events: List[str]) -> List[dict]:
    """
    Pre-formatting the events to get a dict that contains the date, the name, and the description

    Inputs:
        events: Dataframe of all events (needed to get the date)
        important_events: List containing the 3 most important events
    Output:
        list of dict where each dict describes an event by their name, a little description and its date

    """
    events_list = []
    grouped = events.groupby("Event")
    for event in important_events:
        describe_prompt = f"Describe this economic event in one sentence: {event}"
        description = ask_GPT(describe_prompt)
        date = grouped.get_group(event)['Date'].iloc[-1]
        event_dict = {
            "name": event,
            "description" : description,
            "date": date
        }
        events_list.append(event_dict)
    return events_list

def format_events(described_events: List[dict], is_past_event: bool) -> str:
    """
    Create the HTML code to illustrate the events
    
    Inputs:
        described_events : List of dict of the 3 important economics (each dict contains the "date","name","description" keys)
        is_past_event: bool -> True if looking at past events, else false
        
    Output:
        HTML list items stored in a string
    """
    #create review event function
    if is_past_event:
        html_class = "prev_event"
    else:
        html_class = "event"
    HTML = ""
    for event in described_events:
        HTML = HTML + f"""<li class={html_class} data-date={event["date"]}><h3>{event["name"]}</h3><p>{event["description"]}</p></li>"""
    return HTML


def previous_event(portfolio_allocation) -> str:
    """
    Getting all the events in the past week and formatting the information to fit it to the portfolio

    Input:
        portfolio_allocation: Dictionnary where the keys are the stock tickers and the values are the percentage of each one in this portfolio
    
    Output:
        events_html: Formatted HTML code of the events in the past week that we impactful to the portfolio (str)
    """
    days_before = -7
    previous_events_df = get_events(days_before)
    
    important_events = review_events(previous_events_df, portfolio_allocation)
    described_events = describe_events(previous_events_df, important_events)
    events_html = format_events(described_events, True)
    return events_html

def upcomming_event(portfolio_allocation) -> str:
    """
    Getting all the events in the upcomming week and formatting the information to fit it to the portfolio

    Input:
        portfolio_allocation: Dictionnary where the keys are the stock tickers and the values are the percentage of each one in this portfolio
    
    Output:
        events_html: Formatted HTML code of the events in the upcomming week that we impactful to the portfolio (str)
    """
    events_df = get_events(7)
    important_events = review_events(events_df, portfolio_allocation)
    described_events = describe_events(events_df, important_events)
    events_html = format_events(described_events, False)
    return events_html