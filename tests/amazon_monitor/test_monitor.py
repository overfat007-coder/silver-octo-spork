import asyncio

import pytest

pytest.importorskip("aiohttp")

from tools.amazon_price_monitor.config import MonitorConfig
from tools.amazon_price_monitor.monitor import PriceMonitor


def test_notifies_on_threshold_cross(monkeypatch) -> None:
    cfg = MonitorConfig(
        check_interval_minutes=10,
        target_price=100,
        telegram_bot_token="t",
        telegram_chat_id="c",
        user_agents=["ua"],
        proxies=[],
    )

    monitor = PriceMonitor(cfg, ["https://example.com/item"])

    class DummySession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_):
            return None

    sent = []

    async def fake_fetch_snapshot(_session, _url):
        from tools.amazon_price_monitor.models import ProductSnapshot

        return ProductSnapshot(url="https://example.com/item", title="Item", price=99.0, currency="$")

    async def fake_send(_token, _chat, text):
        sent.append(text)

    monkeypatch.setattr("tools.amazon_price_monitor.monitor.aiohttp.ClientSession", lambda timeout: DummySession())
    monkeypatch.setattr(monitor, "_fetch_snapshot", fake_fetch_snapshot)
    monkeypatch.setattr("tools.amazon_price_monitor.monitor.send_telegram_message", fake_send)

    asyncio.run(monitor.check_once())
    assert len(sent) == 1
