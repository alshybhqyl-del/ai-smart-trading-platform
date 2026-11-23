from app.risk import position_size
import pytest

def test_position_size():
    result = position_size(1000, 1, 100, 90)
    assert result["risk_amount"] == 10
    assert result["quantity"] == 1

def test_rejects_high_risk():
    with pytest.raises(ValueError):
        position_size(1000, 3, 100, 90)
