# Binance Price Alert

Real-time crypto price monitor with alerts for Binance spot pairs.
Live candlestick charts, dark/light theme, and price change notifications.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Features

- Live price table for any Binance USDT pair (WebSocket)
- Candlestick chart with volume bars (5m / 15m / 1h / 4h / 1d)
- Price change alerts with configurable threshold and time window
- Dark / light theme

---

## Install

```bash
npx binance-price-alert
```

Open **http://localhost:8000** in your browser.

---

## Run from source

```bash
git clone https://github.com/oottoo/binance-price-alert.git
cd binance-price-alert
pip install -r requirements.txt
python main.py
```

---

## Configuration

Edit `config.yaml` (created automatically on first run):

```yaml
symbols:
  - BTC
  - ETH
  - BNB

alert_threshold: 1        # % change to trigger an alert
alert_window_min: 5       # lookback window in minutes
poll_interval: 10         # seconds between price checks
reset_hour: 0             # hour (UTC) to reset daily stats
```

Settings can also be changed live from the **⚙ Settings** panel in the UI.

---

Made with ♥ by [420.vet](https://420.vet)
