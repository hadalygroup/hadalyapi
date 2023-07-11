from typing import List
from reports.generate_content import generate_HTML
from util.last_open_day import get_previous_open_day
from util.market_data import get_data_yfinance as get_market_data
from reports.sections.Risk.get_beta_data import get_betas
from reports.sections.General_description.important_stocks import important_stocks

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import time
import datetime as dt

def generate_report(portfolio: dict):
    today = dt.date.today()
    day_before = get_previous_open_day(today)
    day_before = day_before.strftime('%Y-%m-%d')
    today = today.strftime('%Y-%m-%d')
    portfolio_total_value = 0
    stocks_value = {}
    for stock, n_stock in portfolio.items():
        OHLC = get_market_data(stock, day_before, today, "1d")
        portfolio_total_value += OHLC["close"] * n_stock
        stocks_value[stock] = n_stock * OHLC["close"]
    
    portfolio_allocation = {}
    for stock, amount in stocks_value.items():
        portfolio_allocation[stock] = amount * 100 /portfolio_total_value

    time.sleep(5)

    stock_betas, portfolio_beta = get_betas(portfolio_allocation)
    
    html = generate_HTML( #debug here
            portfolio=portfolio,
            portfolio_value=portfolio_total_value,
            important_stocks= important_stocks(portfolio_allocation),
            portfolio_allocation = portfolio_allocation,
            portfolio_beta= portfolio_beta,
            betas=stock_betas
            )
    
    filename = f"./reports/generated_reports/hadaly-report-{time.time()}.pdf"

    font_config = FontConfiguration()

    css = CSS(filename="./reports/report.css")
    html_obj = HTML(string=html, base_url=".")
    html_obj.write_pdf(
        filename, stylesheets=[css],
        font_config=font_config)

    
    return