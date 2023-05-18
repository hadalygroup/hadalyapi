from datetime import datetime, timedelta

def getPreviousDay(date: str)->str:
    date = datetime.strptime(date, "%Y-%m-%d")
    previous_day = str(date - timedelta(days=1))
    return previous_day
