import time
import Indicators
from datetime import datetime, timedelta

import ccxt
import pandas as pd
binance = ccxt.binance({
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'
timeframe = '1m'
limit = 1000

now = datetime.now()
end_time = int(now.timestamp() * 1000)
start_time = int((now - timedelta(days=365)).timestamp() * 1000)

data = []
print("Now getting historical prices...")

while start_time < end_time:
    ohlcv = binance.fetch_ohlcv(symbol, timeframe=timeframe, since=start_time, limit=limit)
    data.extend(ohlcv)
    start_time = ohlcv[-1][0] + 1
    time.sleep(binance.rateLimit / 1000)

#history data
df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('datetime', inplace=True)

df.to_csv("HistoryPrice.csv")

#add indicators
Indicate_df = pd.read_csv("HistoryPrice.csv")
Indicate_df = Indicators.addd_indicators(Indicate_df)

daily_df = Indicators.extract_daily_features(Indicate_df)
daily_df.to_csv("daily_features.csv")