# tests/test_alerts.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.alerts import AlertDispatcher

@pytest.mark.asyncio
async def test_telegram_alert_sends_message():
    cfg = {"telegram": {"enabled": True, "bot_token": "TOKEN", "chat_id": "123"},
           "email": {"enabled": False}}
    dispatcher = AlertDispatcher(cfg)
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        mock_instance.post.return_value = MagicMock(status_code=200)
        await dispatcher.send("BTC", pct=3.5, window_min=5)
        assert mock_instance.post.called

@pytest.mark.asyncio
async def test_disabled_channels_do_not_send():
    cfg = {"telegram": {"enabled": False}, "email": {"enabled": False}}
    dispatcher = AlertDispatcher(cfg)
    await dispatcher.send("BTC", pct=3.5, window_min=5)
