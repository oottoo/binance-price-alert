import asyncio
import json
import logging
from datetime import datetime
from typing import Set

from fastapi.websockets import WebSocket

from app.binance import BinanceClient
from app.tracker import PriceTracker
from app.alerts import AlertDispatcher
from app.config import load_config

logger = logging.getLogger(__name__)

class PriceScheduler:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.connections: Set[WebSocket] = set()
        self.alert_history: list = []
        self._task: asyncio.Task | None = None
        self._day_opens: dict = {}
        self._reload_config()

    def _reload_config(self):
        cfg = load_config(self.config_path)
        self.config = cfg
        self.client = BinanceClient(cfg["symbols"])
        self.tracker = PriceTracker(
            threshold_pct=cfg["alert_threshold"],
            window_min=cfg["alert_window_min"],
        )
        self.dispatcher = AlertDispatcher(cfg)

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.add(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.discard(ws)

    async def _broadcast(self, data: dict):
        dead = set()
        for ws in self.connections:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.add(ws)
        self.connections -= dead

    async def _refresh_day_opens(self):
        reset_hour = self.config.get("reset_hour", 0)
        for sym in self.config["symbols"]:
            try:
                self._day_opens[sym] = await self.client.get_price_at_open(sym, reset_hour)
            except Exception as e:
                logger.warning(f"Could not fetch day open for {sym}: {e}")
                self._day_opens.setdefault(sym, 0.0)

    async def run(self):
        await self._refresh_day_opens()
        last_open_date = datetime.now().date()

        while True:
            try:
                today = datetime.now().date()
                if today != last_open_date:
                    await self._refresh_day_opens()
                    last_open_date = today

                prices_raw = await self.client.get_prices()

                for sym, price_data in prices_raw.items():
                    self.tracker.record(sym, price_data)
                    snap = self.tracker.get_snapshot(sym, self._day_opens.get(sym, 0.0))
                    if snap["spike_alert"]:
                        alert = {
                            "symbol": sym,
                            "pct": snap["change_spike_pct"],
                            "window_min": self.config["alert_window_min"],
                            "timestamp": datetime.now().isoformat(),
                        }
                        self.alert_history.insert(0, alert)
                        self.alert_history = self.alert_history[:20]
                        await self.dispatcher.send(
                            sym, snap["change_spike_pct"], self.config["alert_window_min"]
                        )

                snapshots = [
                    self.tracker.get_snapshot(sym, self._day_opens.get(sym, 0.0))
                    for sym in self.config["symbols"]
                ]

                await self._broadcast({
                    "timestamp": datetime.now().isoformat(),
                    "prices": snapshots,
                    "alerts": self.alert_history,
                })

            except Exception as e:
                logger.error(f"Scheduler error: {e}")

            await asyncio.sleep(self.config.get("poll_interval", 5))

    def start(self):
        self._task = asyncio.create_task(self.run())

    def reload(self):
        self._reload_config()
