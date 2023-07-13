from reports.generate_content import generate_HTML
from util.last_open_day import get_previous_open_day
from util.market_data import get_data_yfinance as get_market_data
from reports.sections.Risk.get_beta_data import get_betas
from reports.sections.General_description.important_stocks import important_stocks
from pydantic import EmailStr
from typing import List

import smtplib
import ssl
from email.message import EmailMessage
import os

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import time
import datetime as dt
from reports.graphs.generateGraphs import generate_graphs

async def generate_report(portfolio: dict, receiver_email: str):
    report_id = time.time()

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
        portfolio_allocation[stock] = amount[0] * 100 /portfolio_total_value[0]

    portfolio_total_value = round(portfolio_total_value[0], 2)

    time.sleep(5)

    stock_betas, portfolio_beta = get_betas(portfolio_allocation)
 
    generate_graphs(portfolio_allocation, portfolio, portfolio_beta, report_id)
    
    html = generate_HTML(
            portfolio=portfolio,
            portfolio_value=portfolio_total_value,
            important_stocks= important_stocks(portfolio_allocation),
            portfolio_allocation = portfolio_allocation,
            portfolio_beta= portfolio_beta,
            betas=stock_betas,
            report_id=report_id
            )
    
    filename = f"./reports/generated_reports/hadaly-report-{report_id}.pdf"

    font_config = FontConfiguration()

    css = CSS(filename="./reports/report.css")
    html_obj = HTML(string=html, base_url=".")
    html_obj.write_pdf(
            filename, stylesheets=[css],
            font_config=font_config)
    
    template = """
        <html>
        <body>
         
 
        <p>Hi !!!
        <br>Thanks for using fastapi mail, keep using it..!!!</p>
 
 
        </body>
        </html>
        """


    
    sender_email = os.environ.get("MAIL_FROM")
    sender_password= os.environ.get("MAIL_PASSWORD")
    subject = 'Your Hadaly portfolio report'
    body = """
    Here is your Hadaly Report
    """
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    with open(filename, 'rb') as content_file:
        content = content_file.read()
        em.add_attachment(content, maintype='application', subtype='pdf', filename=f"hadaly-report-{report_id}.pdf")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
        # Log in to your Gmail account
    server.login(sender_email, sender_password)
    server.send_message(em)
    print(" ~~ Mail has been sent :) ~~ ")
    return