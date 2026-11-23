import pandas as pd

def enrich(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    close, high, low = x.close, x.high, x.low
    x["ema20"] = close.ewm(span=20, adjust=False).mean()
    x["ema50"] = close.ewm(span=50, adjust=False).mean()
    x["ema200"] = close.ewm(span=200, adjust=False).mean()
    delta = close.diff()
    gain, loss = delta.clip(lower=0), -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, adjust=False).mean().replace(0, 1e-12)
    rs = avg_gain / avg_loss
    x["rsi"] = 100 - (100 / (1 + rs))
    fast = close.ewm(span=12, adjust=False).mean()
    slow = close.ewm(span=26, adjust=False).mean()
    x["macd"] = fast - slow
    x["macd_signal"] = x.macd.ewm(span=9, adjust=False).mean()
    tr = pd.concat([(high-low), (high-close.shift()).abs(), (low-close.shift()).abs()], axis=1).max(axis=1)
    x["atr"] = tr.rolling(14).mean()
    x["vol_sma20"] = x.volume.rolling(20).mean()
    return x

def signal(df: pd.DataFrame):
    if len(df) < 200:
        return {"action":"HOLD","confidence":0,"reason":"بيانات غير كافية (نحتاج 200 شمعة على الأقل)"}
    x = enrich(df).iloc[-1]
    checks = [
        x.close > x.ema200,
        x.ema20 > x.ema50,
        x.macd > x.macd_signal,
        45 < x.rsi < 70,
        x.volume > x.vol_sma20
    ]
    score = int(sum(bool(v) for v in checks) / len(checks) * 100)
    action = "BUY" if score >= 80 else "HOLD"
    return {
        "action": action, "confidence": score,
        "entry": round(float(x.close), 8),
        "stop_loss": round(float(x.close - 2*x.atr), 8) if pd.notna(x.atr) else None,
        "take_profit": round(float(x.close + 4*x.atr), 8) if pd.notna(x.atr) else None,
        "indicators": {"rsi": round(float(x.rsi),2), "ema20": float(x.ema20),
                       "ema50": float(x.ema50), "ema200": float(x.ema200),
                       "macd": float(x.macd), "atr": float(x.atr)},
        "reason": "درجة توافق مؤشرات تجريبية؛ لا تمثل احتمال ربح إحصائيًا."
    }
