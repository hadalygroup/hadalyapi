import datetime
import yfinance as yf
from util.calculate_return import calculate_return

def calculate_sp500_return(time: int):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=time)

    sp500_data = yf.download('^GSPC', start=start_date, end=end_date, progress=False)
    initial = sp500_data['Close'][0]
    final = sp500_data['Close'][-1]
    return calculate_return(initial,final)