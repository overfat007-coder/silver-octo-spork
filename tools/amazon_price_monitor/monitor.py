import asyncio
import logging
from typing import Awaitable, Callable

import aiohttp

from tools.amazon_price_monitor.config import MonitorConfig
from tools.amazon_price_monitor.fetchers import RequestRotator, fetch_html_aiohttp, fetch_html_playwright
from tools.amazon_price_monitor.models import MonitorState, ProductSnapshot
from tools.amazon_price_monitor.parser import extract_snapshot
from tools.amazon_price_monitor.telegram import send_telegram_message

logger = logging.getLogger("amazon_price_monitor")


class PriceMonitor:
    def __init__(self, config: MonitorConfig, urls: list[str]) -> None:
        self.config = config
        self.urls = urls
        self.states: dict[str, MonitorState] = {url: MonitorState() for url in urls}
        self.rotator = RequestRotator(user_agents=config.user_agents or [], proxies=config.proxies or [])

    async def check_once(self) -> list[ProductSnapshot]:
        timeout = aiohttp.ClientTimeout(total=self.config.request_timeout_s)
        snapshots: list[ProductSnapshot] = []

        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [self._fetch_snapshot(session, url) for url in self.urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    logger.warning("fetch failed: %s", result)
                    continue
                snapshots.append(result)

        for snap in snapshots:
            state = self.states[snap.url]
            should_notify = snap.price <= self.config.target_price and (
                state.last_price is None or state.last_price > self.config.target_price
            )
            if should_notify:
                text = (
                    f"📉 Price alert!\n"
                    f"{snap.title}\n"
                    f"Price: {snap.currency}{snap.price:.2f}\n"
                    f"Threshold: {self.config.target_price:.2f}\n"
                    f"URL: {snap.url}"
                )
                await send_telegram_message(self.config.telegram_bot_token, self.config.telegram_chat_id, text)
            state.last_price = snap.price

        return snapshots

    async def _fetch_snapshot(self, session: aiohttp.ClientSession, url: str) -> ProductSnapshot:
        html = await fetch_html_aiohttp(session, url, self.rotator)
        try:
            return extract_snapshot(url, html)
        except Exception:
            if not self.config.dynamic_enabled:
                raise
            html_js = await fetch_html_playwright(url, self.rotator.pick_user_agent())
            return extract_snapshot(url, html_js)

    async def run_forever(self) -> None:
        while True:
            await self.check_once()
            await asyncio.sleep(self.config.check_interval_minutes * 60)


async def run_from_files(config_path: str, urls_path: str) -> None:
    from tools.amazon_price_monitor.config import load_config, load_urls

    config = load_config(config_path)
    urls = load_urls(urls_path)
    monitor = PriceMonitor(config=config, urls=urls)
    await monitor.run_forever()
