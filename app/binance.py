import httpx
import asyncio
from typing import Dict

BASE_URL = "https://api.binance.com/api/v3"

SYMBOL_MAP = {
    "BNB": "BNBUSDT", "BTC": "BTCUSDT", "VET": "VETUSDT",
    "VTHO": "VTHOUSDT", "ETH": "ETHUSDT",
}

class BinanceClient:
    def __init__(self, symbols: list[str]):
        self.symbols = symbols

    async def _fetch_price(self, symbol: str) -> float:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{BASE_URL}/ticker/price", params={"symbol": symbol})
            r.raise_for_status()
            return float(r.json()["price"])

    async def get_prices(self) -> Dict[str, dict]:
        pairs = [SYMBOL_MAP[s] for s in self.symbols if s in SYMBOL_MAP]
        pairs.append("EURUSDT")

        tasks = {sym: self._fetch_price(sym) for sym in pairs}
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw = dict(zip(tasks.keys(), results))

        eur_usdt = raw.get("EURUSDT", 1.0)
        if isinstance(eur_usdt, Exception):
            eur_usdt = 1.0

        prices = {}
        for sym in self.symbols:
            pair = SYMBOL_MAP.get(sym)
            if not pair:
                continue
            val = raw.get(pair, 0.0)
            if isinstance(val, Exception):
                val = 0.0
            prices[sym] = {
                "usdt": val,
                "eur": val / eur_usdt if eur_usdt else 0.0,
            }
        return prices

    async def get_price_at_open(self, symbol: str, reset_hour: int) -> float:
        from datetime import datetime, timedelta
        pair = SYMBOL_MAP.get(symbol, "BTCUSDT")
        now = datetime.now()
        open_dt = now.replace(hour=reset_hour, minute=0, second=0, microsecond=0)
        if open_dt > now:
            open_dt -= timedelta(days=1)
        start_ms = int(open_dt.timestamp() * 1000)
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                f"{BASE_URL}/klines",
                params={"symbol": pair, "interval": "1m", "startTime": start_ms, "limit": 1}
            )
            r.raise_for_status()
            data = r.json()
            if data:
                return float(data[0][1])
        return 0.0
