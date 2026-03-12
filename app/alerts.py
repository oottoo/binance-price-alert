import smtplib
import httpx
from email.mime.text import MIMEText
from datetime import datetime


class AlertDispatcher:
    def __init__(self, config: dict):
        self.config = config

    async def send(self, symbol: str, pct: float, window_min: int) -> None:
        direction = "subio" if pct > 0 else "cayo"
        msg = (
            f"ALERTA: {symbol} {direction} {abs(pct):.2f}% "
            f"en los ultimos {window_min} min ({datetime.now().strftime('%H:%M:%S')})"
        )
        await self._send_telegram(msg)
        self._send_email(msg)

    async def _send_telegram(self, text: str) -> None:
        tg = self.config.get("telegram", {})
        if not tg.get("enabled"):
            return
        url = f"https://api.telegram.org/bot{tg['bot_token']}/sendMessage"
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(url, json={"chat_id": tg["chat_id"], "text": text})

    def _send_email(self, text: str) -> None:
        em = self.config.get("email", {})
        if not em.get("enabled"):
            return
        msg = MIMEText(text)
        msg["Subject"] = "Trade Alert"
        msg["From"] = em["user"]
        msg["To"] = em["to"]
        with smtplib.SMTP(em["smtp_host"], em["smtp_port"]) as server:
            server.starttls()
            server.login(em["user"], em["password"])
            server.send_message(msg)
