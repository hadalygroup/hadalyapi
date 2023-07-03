import requests
import pandas as pd
import datetime as dt
from typing import Union, List, Optional

def get_economic_calendar(
    countries: Union[List[str], str] = "",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """Get economic calendar for countries between specified dates

    Parameters
    ----------
    countries : [List[str],str]
        List of countries to include in calendar.  Empty returns all
    start_date : Optional[str]
        Start date for calendar
    end_date : Optional[str]
        End date for calendar

    Returns
    -------
    pd.DataFrame
        Economic calendar

    Examples
    --------
    Get todays economic calendar for the United States
    >>> from openbb_terminal.sdk import openbb
    >>> calendar = openbb.economy.events("united_states")

    To get multiple countries for a given date, pass the same start and end date as well as
    a list of countries
    >>> calendars = openbb.economy.events(["united_states", "canada"], start_date="2022-11-18", end_date="2022-11-18")
    """

    if start_date is None:
        start_date = dt.date.today().strftime("%Y-%m-%d")

    if end_date is None:
        end_date = dt.date.today().strftime("%Y-%m-%d")

    if countries == "":
        countries = []
    if isinstance(countries, str):
        countries = [countries]

    countries = [country.replace("_", " ").title() for country in countries]

    if start_date == end_date:
        dates = [start_date]
    else:
        dates = (
            pd.date_range(start=start_date, end=end_date).strftime("%Y-%m-%d").tolist()
        )
    calendar = pd.DataFrame()
    for date in dates:
        try:
            df = pd.DataFrame(
                requests.get(
                    f"https://api.nasdaq.com/api/calendar/economicevents?date={date}",
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
                    } 
                ).json()["data"]["rows"]
            ).replace("&nbsp;", "-")
            df.loc[:, "Date"] = date
            calendar = pd.concat([calendar, df], axis=0)
        except TypeError:
            continue

    if calendar.empty:
        print("[red]No data found for date range.[/red]")
        return pd.DataFrame()

    calendar = calendar.rename(
        columns={
            "gmt": "Time (ET)",
            "country": "Country",
            "eventName": "Event",
            "actual": "Actual",
            "consensus": "Consensus",
            "previous": "Previous",
        }
    )

    calendar = calendar.drop(columns=["description"])
    if not countries:
        return calendar

    calendar = calendar[calendar["Country"].isin(countries)].reset_index(drop=True)
    if calendar.empty:
        print(f"[red]No data found for {', '.join(countries)}[/red]")
        return pd.DataFrame()
    return calendar