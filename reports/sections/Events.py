import datetime
from util.events import get_economic_calendar as get_events
from util.ask_gpt import ask_GPT
import ast

def get_upcomming_events():
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    today = today.strftime('%Y-%m-%d')
    next_week = next_week.strftime('%Y-%m-%d')
    upcoming_events = get_events(start_date=today,end_date=next_week)
    return upcoming_events['Event'].tolist()

def get_past_events():
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    today = today.strftime('%Y-%m-%d')
    last_week = last_week.strftime('%Y-%m-%d')
    upcoming_events = get_events(start_date=last_week,end_date=today)
    return upcoming_events['Event'].tolist()

def review_past_events(portfolio_allocation):
    past_events_prompt = f"""Here is a list of the economic events that happened this week,
    I want a python list of the 3 most importants for a portfolio with this allocation of stocks {portfolio_allocation}.
    {get_past_events()}
    """
    return ask_GPT(past_events_prompt)

def review_upcomming_events(portfolio_allocation):
    upcomming_events_prompt = f"""Here is a list of the economic events in the upcoming week,
    I want a python list of the 3 most importants for a portfolio with this allocation of stocks {portfolio_allocation}.
    {get_upcomming_events()}
    """
    return ask_GPT(upcomming_events_prompt)