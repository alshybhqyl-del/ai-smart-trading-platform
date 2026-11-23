def position_size(equity: float, risk_pct: float, entry: float, stop: float,
                  max_risk_pct: float = 2.0):
    if equity <= 0 or entry <= 0 or stop <= 0 or entry == stop:
        raise ValueError("Invalid equity, entry or stop")
    if not 0 < risk_pct <= max_risk_pct:
        raise ValueError(f"risk_pct must be >0 and <= {max_risk_pct}")
    risk_amount = equity * risk_pct / 100
    quantity = risk_amount / abs(entry - stop)
    return {"risk_amount": round(risk_amount, 8),
            "quantity": round(quantity, 8),
            "notional": round(quantity * entry, 8)}
