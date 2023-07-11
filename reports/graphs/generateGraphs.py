import pandas as pd
import plotly.graph_objects as go
from util.sp500_performance import get_stock_data_monthly as stock_data
from util.calculate_return import calculate_return
from plotly.io import write_image

DONUT_COLORS = ['#f992ad', '#fbbcee', '#fab4c8', '#f78ecf', '#cfb9f7', '#e0cefd', '#a480f2', '#d4b0f9', '#c580ed', '#d199f1']
BENCHMARK_COLORS = ["#ffc7fb", "#4d4d4d"]
MONTHS_STR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def add_lists(lists):
    result = []
    for items in zip(*lists):
        total = sum(items)
        result.append(total)
    return result

def generate_graphs(portfolio_allocation: dict, portfolio: dict, beta: float, report_id: float):
    generate_donut(portfolio_allocation, report_id)

    generate_benchmark(portfolio, report_id)

    generate_beta(beta, report_id)
    return

def generate_donut(portfolio_allocation: dict, report_id: float):
    print(portfolio_allocation)
    filename = f"./reports/graphs/donut-{report_id}.png"
    fig = go.Figure(data=[go.Pie(labels=list(portfolio_allocation.keys()), values=list(portfolio_allocation.values()), hole=.4)])
    fig.update_traces(marker=dict(colors=DONUT_COLORS))
    fig.update_layout(autosize=False, height=400, width=420)
    fig.update_layout(
        margin=dict(l=10, r=0, t=0, b=0),
    )
    write_image(fig, filename,"png")
    return
    
def generate_benchmark(portfolio: dict, report_id: float):
    filename = f"./reports/graphs/benchmark-{report_id}.png"

    sp500 = stock_data('^GSPC',13)
    portfolio_value = []
    for stock, n_stock in portfolio.items():
        multiplied_stock_year = []
        stock_year = stock_data(stock, 13)
        for value in stock_year:
            multiplied_stock_year.append(value * n_stock)
        portfolio_value.append(multiplied_stock_year)
    
    portfolio_value = add_lists(portfolio_value)
  

    portfolio_track = []
    sp500_track = []

    for index, value in enumerate(sp500):
        if index == 0:
            continue
        sp500_track.append(calculate_return(sp500[index-1], value))
    for index, value in enumerate(portfolio_value):
        if index == 0:
            continue
        portfolio_track.append(calculate_return(portfolio_value[index-1], value))
    
    benchmark = go.Figure()
    benchmark_df = pd.DataFrame({
        "Months": MONTHS_STR,
        "SP500" : sp500_track,
        "Portfolio": portfolio_track
    })

    benchmark.add_trace(go.Scatter(x=benchmark_df["Months"], y=benchmark_df["SP500"],
                        line = {"color":BENCHMARK_COLORS[1]},
                        mode='lines+markers',
                        line_shape='spline',
                        name='SP500'))
    benchmark.add_trace(go.Scatter(x=benchmark_df["Months"], y=benchmark_df["Portfolio"],
                        line = {"color":BENCHMARK_COLORS[0]},
                        mode='lines+markers',
                        line_shape='spline',
                        name='Your Portfolio'))
    benchmark.update_xaxes(title_text="Months")
    benchmark.update_yaxes(title_text="Return")
    benchmark.update_layout(autosize=False, height=350)
    benchmark.update_layout(
        margin=dict(l=50, r=50, t=10, b=40),
    )
    #benchmark.write_image(filename)
    write_image(benchmark, filename,"png")
    return

def generate_beta(beta:float, report_id: float):
    filename = f"./reports/graphs/beta-{report_id}.png"
    fig = go.Figure(go.Indicator(
    mode = "number+gauge", value = beta,
    domain = {'x': [0.1, 1], 'y': [0, 1]},
    title = {'text' :"<b>Beta</b>"},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [0, 2]},
        'threshold': {
            'line': {'color': "#000000", 'width': 2.2},
            'thickness': 0.8, 'value': beta},
        'steps': [
            {'range': [0, 0.5], 'color': "#ff6666"},
            {'range': [0.5, 1.5], 'color': "#b3ffab"},
            {'range': [1.5, 2], 'color': "#ff6666"}],
        'bar': {'color': "black", 
                'thickness': 0,
                }}))
    fig.update_layout(autosize=False, height=200, width= 800)
    fig.update_layout(
        margin=dict(l=50, r=50, t=40, b=40),
    )
    #fig.write_image(f"./graphs/beta-{report_id}.png")
    write_image(fig, filename,"png")
    return