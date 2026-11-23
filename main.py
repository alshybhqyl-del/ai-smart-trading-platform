import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .market import fetch_klines
from .strategy import signal
from .risk import position_size

app = FastAPI(title="AI Smart Trading Platform API", version="0.1.0")
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET","POST"],
                   allow_headers=["Content-Type"], allow_credentials=False)

class SizeRequest(BaseModel):
    equity: float = Field(gt=0)
    risk_pct: float = Field(gt=0, le=2)
    entry: float = Field(gt=0)
    stop: float = Field(gt=0)

@app.get("/health")
def health():
    return {"status":"ok", "mode":os.getenv("TRADING_MODE","demo"), "live_trading_enabled":False}

@app.get("/api/market/klines")
async def klines(symbol: str="BTCUSDT", interval: str="15m", limit: int=200):
    try:
        df = await fetch_klines(symbol, interval, limit)
        return df.tail(100).to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Market data unavailable: {str(e)[:180]}")

@app.get("/api/signals")
async def signals(symbol: str="BTCUSDT", interval: str="15m"):
    try:
        df = await fetch_klines(symbol, interval, 500)
        result = signal(df)
        return {"symbol":symbol.upper(), "interval":interval, "mode":"DEMO",
                "live_execution":False, **result}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Signal generation failed: {str(e)[:180]}")

@app.post("/api/risk/position-size")
def size(req: SizeRequest):
    try:
        return position_size(req.equity, req.risk_pct, req.entry, req.stop)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
