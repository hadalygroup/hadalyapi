from datetime import datetime, timedelta

def getPreviousDay(date: str)->str:
    date = datetime.strptime(date, "%Y-%m-%d")
    previous_day = date - timedelta(days=1)
    previous_day = previous_day.strftime("%Y-%m-%d")
    return previous_day
