import datetime

def get_previous_open_day(date: datetime.date) -> str:
    """
    Get the last weekday before the date

    Input: 
        date: datetime.date object
    """

    date = date - datetime.timedelta(days=1)
    while date.weekday() >= 5:  # 5 and 6 represent Saturday and Sunday
        date -= datetime.timedelta(days=1)
    return date