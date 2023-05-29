from engine.strategy import Strategy
from engine.engine import Hadaly_Engine
import json
import plotly.graph_objs as go
from util.calculateIndicators import getOptionnalParams, calculateIndicator
from util.market_data import historical_data_gmd
strategyString = """
{"EXIT": {"LOGIC": [{"RSI": {"time": "0", "source": "close", "timeperiod": "14"}}, {" > ": {}}, {"50": {"num": "50"}}], "EXPOSURE": "1000", "INDICATORS": [{"RSI": {"time": "0", "source": "close", "timeperiod": "14"}}]}, "ENTRY": {"LOGIC": [{"MIDPRICE": {"time": "0", "timeperiod": "14"}}, {" crossover ": {}}, {"MIDPOINT": {"time": "0", "source": "close", "timeperiod": "14"}}, {" and ": {}}, {"RSI": {"time": "0", "source": "close", "timeperiod": "14"}}, {" < ": {}}, {"45": {"num": "45"}}], "EXPOSURE": "1000", "INDICATORS": [{"MIDPRICE": {"time": "0", "timeperiod": "14"}}, {"MIDPOINT": {"time": "0", "source": "close", "timeperiod": "14"}}, {"RSI": {"time": "0", "source": "close", "timeperiod": "14"}}]}, "SECURITY": {"stop_loss": {"status": 1, "value": "3"}, "take_profit": {"status": 1, "value": "10"}, "trailing_stop": {"status": 1, "value": "3"}}}
"""
# start_time = timeit.default_timer()
# indicator = {'RSI': {'time': '1', 'source': 'close', 'timeperiod': '15'}}
# data = historical_data_gmd("AAPL","2022-01-01", "2022-01-31", "1d")
# if (data):
#     print("we got data")
# d1 = calculateIndicator(data, indicator)
# d2 = calculateIndicator(data, "RSI")

# elapsed = timeit.default_timer() - start_time
# print(elapsed)

# print(type(d2))
strategy = Strategy(strategyString)
jsons =json.loads(strategyString)
# a = []
# for i in jsons["ENTRY"]["INDICATORS"]:
#     for key in i.keys():
#         a.append(key)

# print(a)


def prepare_list_for_bot_action(y1,y2):
  mult=[y1[i] * y2[i] for i in range(len(y1))]
  show=[i if i!=0 else None for i in mult]
  return show


def plot_backtest_hp(data, start,end):
    bc="#16161a"
    grid_color=	'#36454f'
    width=1.5
    smoothing=1
    adj_stock_price=[i/data['stock_price'][data['start_date_index']]*1000 for i in data['stock_price']]
    nbuy_move=prepare_list_for_bot_action(adj_stock_price,data['buy_move'])
    nsell_move=prepare_list_for_bot_action(adj_stock_price,data['sell_move'])

    layout= {'dragmode':"pan","plot_bgcolor": bc,"paper_bgcolor" : bc,"margin" : dict(t=15,b=50,l=40,r=40),
           "legend" :dict(orientation="h",yanchor="bottom",y=1.01,xanchor="left",x=0),
           "xaxis": dict(color="#FFFFFF",gridcolor=grid_color,range=[start,end]),
           "yaxis": dict(color="#FFFFFF",gridcolor=grid_color), 
           'colorway': ['#7f5af0','#2cb67d','#fffffe','#ff8906','#ff8906','#3da9fc'],
           'font': {'color': '#fffffe'}}
    
    fig1= [go.Scatter(x=data['close_time'],
                      y=adj_stock_price,
                      mode='lines+text',
                      line=dict(width=width, shape='spline',smoothing=smoothing),
                      name='Stock price', 
                      text=data['move_info'],
                      textposition="top center",
                      textfont=dict(family='Montserrat',size=17,color='#ffffff')),
          go.Scatter(x=data['close_time'],
                     y=data['port_value'],
                     name='Strategy',
                     line=dict(width=width, shape='spline',smoothing=smoothing)),
          go.Scatter(x=data['close_time'],
                     y=nbuy_move,name='buy_move',
                     mode='markers',
                     marker=dict(color='rgba(44, 182, 125, 0.75)', size= 10)),
          go.Scatter(x=data['close_time'],
                     y=nsell_move,name='sell_move',
                     mode='markers',
                     marker=dict(color='rgba(250, 82, 70, 0.75)', size= 10) )
         ]
    fig = go.Figure(data=fig1, layout=layout)
    return fig.to_json()

start = "2022-01-02"
end = "2022-08-07"

# engine = Hadaly_Engine(strategy,"AAPL", start, end, "1d")
# stockmoney = engine.simulation["stock_wallet"]
# cashmoney = engine.simulation["cash_wallet"]
# portvalue = engine.simulation["port_value"]

with open("./plot.json") as f:
   fig = json.load(f)

figu = go.Figure(fig)
figu.show()
# image = plot_backtest_hp(engine.simulation, start, end)

# with open("./plot.json","w") as f:
#    f.write(image)

#print(engine.simulation)