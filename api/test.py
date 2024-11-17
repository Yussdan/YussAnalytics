import requests
from utils import make_request
from datetime import datetime
import pandas as pd


params = {'fsym': 'BTC', 'tsym': 'USD', 'limit': '10', }
data = make_request(f"v2/histoday", params)

cripto= 'BTC'
action = 'day'
r = requests.get(f'http://127.0.0.1:5000/{cripto}/plot/USD/{action}/10')
print(r.content)
# time = 'day'
# prices = [
#     {
#         "time": datetime.fromtimestamp(info['time']).strftime('%H:%M' if time == 'hour' else '%Y-%m-%d'),
#         "high": info['high'],
#         "low": info['low'],
#         "close": info['close'],
#         "currency": 'USD'
#     }
#     for info in data.get('Data', {}).get('Data', [])
# ]
# df = pd.DataFrame(prices)
# df['percent_change'] = df['close'].pct_change().fillna(0) * 100
print(r.text)