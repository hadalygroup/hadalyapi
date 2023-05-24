from engine.strategy import Strategy
from engine.engine import Hadaly_Engine
import json


strategyString = """
{
	"EXIT": {
		"LOGIC": [{
			"RSI": {
				"time": "0",
				"source": "close",
				"timeperiod": "14"
			}
		}, {
			" > ": {}
		}, {
			"50": {
				"num": "50"
			}
		}],
		"EXPOSURE": "1000",
		"INDICATORS": [{
			"RSI": {
				"time": "0",
				"source": "close",
				"timeperiod": "14"
			}
		}]
	},
	"ENTRY": {
		"LOGIC": [{
			"RSI": {
				"time": "0",
				"source": "close",
				"timeperiod": "14"
			}
		}, {
			" > ": {}
		}, {
			"45": {
				"num": "45"
			}
		}],
		"EXPOSURE": "1000",
		"INDICATORS": [{
			"MIDPRICE": {
				"time": "0",
				"timeperiod": "14"
			}
		}, {
			"MIDPOINT": {
				"time": "0",
				"source": "close",
				"timeperiod": "14"
			}
		}, {
			"RSI": {
				"time": "0",
				"source": "close",
				"timeperiod": "14"
			}
		}]
	},
	"SECURITY": {
		"stop_loss": {
			"status": 1,
			"value": "3"
		},
		"take_profit": {
			"status": 1,
			"value": "10"
		},
		"trailing_stop": {
			"status": 1,
			"value": "3"
		}
	}
}
"""

strategy = Strategy(strategyString)
# jsons =json.loads(strategyString)
# a = []
# for i in jsons["ENTRY"]["INDICATORS"]:
#     for key in i.keys():
#         a.append(key)
    
# print(a)

engine = Hadaly_Engine(strategy,"AAPL", "2022-09-02", "2023-03-07","1d")
stockmoney = engine.simulation['stock_wallet']
cashmoney = engine.simulation['cash_wallet']
portvalue = engine.simulation['port_value']

print(engine.simulation)