import pandas as pd
import pandas_ta as ta

def addd_indicators(df: pd.DataFrame) -> pd.DataFrame:
    #RSI
    df["rsi_14"] = ta.rsi(df["close"], length=14)

    #Moving Average
    df["ma_7"] = ta.ma(df["close"], length=7)
    df["ma_21"] = ta.ma(df["close"], length=21)

    #MACD
    macd = ta.macd(df["close"])
    df["macd"] = macd["MACD_12_26_9"]

    #Bollinger Bands
    bb = ta.bbands(df["close"], length=20)
    df["bb_upper"] = bb["BBU_20_2.0"]
    df["bb_lower"] = bb["BBL_20_2.0"]

    return df


def extract_daily_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["datetime"]).dt.date

    grouped = df.groupby(["date"])
    daily = grouped.agg({
        "close": ["first", "last", "mean"],
        "volume": ["sum", "std"],
        "rsi_14": "mean",
        "ma_7": "last",
        "macd": "mean",
        "bb_upper": "max",
        "bb_lower": "min"
    })

    daily.columns = ["_".join(col) for col in daily.columns]
    daily.reset_index(inplace=True)

    daily["close_return"] = daily["close_last"].pct_change()
    daily["volume_growth"] = daily["volume_sum"].pct_change()
    daily["rsi_diff"] = daily["rsi_14_mean"].diff()
    daily["price_vs_ma"] = daily["close_last"] / daily["ma_7_last"] - 1
    daily["bb_width"] = daily["bb_upper_max"] - daily["bb_lower_min"]

    return daily
