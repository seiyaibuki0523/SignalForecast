import requests
import pandas as pd
from datetime import datetime

# -------- CryptoPanic --------
def fetch_cryptopanic(auth_token, currencies='BTC'):
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": auth_token,
        "currencies": currencies,
        "filter": "hot",   # hot, rising, bullish, bearish, important, saved, lol
        "kind": "news"     # news / media
    }
    r = requests.get(url, params=params)
    data = r.json().get('results', [])
    rows = []
    for item in data:
        rows.append({
            "source": "cryptopanic",
            "title": item.get("title"),
            "published_at": item.get("published_at"),
            "url": item.get("url"),
            "votes_positive": item.get("votes", {}).get("positive", 0),
            "votes_negative": item.get("votes", {}).get("negative", 0),
            "currencies": ",".join([c["code"] for c in item.get("currencies", [])]) if item.get("currencies") else None
        })
    return pd.DataFrame(rows)

# -------- NewsAPI --------
def fetch_newsapi(api_key, query="bitcoin OR crypto", language="en", page_size=100):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": language,
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": api_key,
    }
    r = requests.get(url, params=params)
    articles = r.json().get("articles", [])
    rows = []
    for a in articles:
        rows.append({
            "source": a["source"]["name"],
            "title": a["title"],
            "published_at": a["publishedAt"],
            "url": a["url"],
            "description": a.get("description"),
            "content": a.get("content")
        })
    return pd.DataFrame(rows)

# -------- Merge --------
def normalize_and_combine(dfs):
    df = pd.concat(dfs, ignore_index=True)
    df["published_at"] = pd.to_datetime(df["published_at"], errors='coerce', utc=True)
    df["date"] = df["published_at"].dt.date
    return df.dropna(subset=["published_at"])
