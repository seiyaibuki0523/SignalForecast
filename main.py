import NewsCatch
import EmotionScore
import pandas as pd

price_daily = pd.read_csv("daily_features.csv")
cryptoPanicToken = ""
newsToken = ""

cp_df = NewsCatch.fetch_cryptopanic(auth_token=cryptoPanicToken)
na_df = NewsCatch.fetch_newsapi(api_key=newsToken)

news_df = NewsCatch.normalize_and_combine([cp_df, na_df])
news_df = EmotionScore.add_sentiment(news_df)
sent_daily = EmotionScore.aggregate_daily_sentiment(news_df)

merged = pd.merge(price_daily, sent_daily, left_on="date", right_on="date", how="left").fillna(0)
merged.to_csv("BTC_Daily_with_Sentiment.csv", index=False)

