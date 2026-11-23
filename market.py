import os
import httpx
import pandas as pd

BASE = os.getenv("BINANCE_BASE_URL", "https://api.binance.com")

async def fetch_klines(symbol="BTCUSDT", interval="15m", limit=200):
    if not symbol.isalnum() or not 1 <= int(limit) <= 1000:
        raise ValueError("Invalid symbol or limit")
    async with httpx.AsyncClient(timeout=12) as client:
        r = await client.get(f"{BASE}/api/v3/klines",
                             params={"symbol": symbol.upper(), "interval": interval, "limit": limit})
        r.raise_for_status()
        raw = r.json()
    cols = ["open_time","open","high","low","close","volume","close_time",
            "quote_volume","trades","taker_buy_base","taker_buy_quote","ignore"]
    df = pd.DataFrame(raw, columns=cols)
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df
