from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def add_sentiment(df):
    def score(text):
        if not isinstance(text, str) or not text.strip():
            return 0
        return analyzer.polarity_scores(text)['compound']
    df["sentiment"] = df["title"].apply(score)
    return df

def aggregate_daily_sentiment(df):
    daily = df.groupby("date").agg(
        sentiment_mean=("sentiment", "mean"),
        sentiment_std=("sentiment", "std"),
        sentiment_count=("sentiment", "count"),
        bullish_votes=("votes_positive", "sum"),
        bearish_votes=("votes_negative", "sum")
    ).reset_index()

    # limit（|score| > 0.6）
    daily["sentiment_extreme_ratio"] = (
        (df["sentiment"].abs() > 0.6).groupby(df["date"]).mean().values
    )
    return daily.fillna(0)
