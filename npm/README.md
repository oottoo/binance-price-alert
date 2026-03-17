# binance-price-alert

Real-time Binance price monitor with candlestick charts and price change alerts.

## Usage

```bash
npx binance-price-alert
```

Then open **http://localhost:8000** in your browser.

> **Windows only.** The pre-built binary runs on Windows x64. To run on macOS/Linux, see [run from source](#run-from-source).

---

## Features

- Live price table for any Binance USDT pair via WebSocket
- Candlestick charts with volume bars — 5m / 15m / 1h / 4h / 1d
- Price change alerts with configurable threshold and time window
- Dark / light theme toggle
- Settings panel — no config file editing required

---

## Configuration

A `config.yaml` is created automatically next to where you run the command on first launch.

```yaml
symbols:
  - BTC
  - ETH
  - BNB

alert_threshold: 1       # % change to trigger an alert
alert_window_min: 5      # lookback window in minutes
poll_interval: 10        # seconds between price checks
reset_hour: 0            # hour (UTC) to reset daily counters
```

All settings can also be changed live from the **⚙ Settings** panel in the UI.

---

## Run from source

Requires Python 3.11+:

```bash
git clone https://github.com/420vet/binance-price-alert.git
cd binance-price-alert
pip install -r requirements.txt
python main.py
```

---

Made with ♥ by [420.vet](https://420.vet)
