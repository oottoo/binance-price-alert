# tests/test_binance.py
import pytest
from unittest.mock import patch
from app.binance import BinanceClient

@pytest.mark.asyncio
async def test_get_prices_returns_expected_symbols():
    mock_responses = {
        "BNBUSDT": 400.0, "BTCUSDT": 65000.0, "VETUSDT": 0.04,
        "VTHOUSDT": 0.008, "ETHUSDT": 3200.0, "EURUSDT": 1.085,
    }

    client = BinanceClient(["BNB", "BTC", "VET", "VTHO", "ETH"])

    async def fake_fetch(symbol):
        return mock_responses.get(symbol, 0.0)

    with patch.object(client, "_fetch_price", side_effect=fake_fetch):
        result = await client.get_prices()

    assert result["BTC"]["usdt"] == 65000.0
    assert round(result["BTC"]["eur"], 2) == round(65000.0 / 1.085, 2)
    assert "VET" in result
    assert "VTHO" in result
