import asyncio
import random
from dataclasses import dataclass

import aiohttp


@dataclass
class RequestRotator:
    user_agents: list[str]
    proxies: list[str]

    def pick_user_agent(self) -> str:
        return random.choice(self.user_agents)

    def pick_proxy(self) -> str | None:
        if not self.proxies:
            return None
        return random.choice(self.proxies)


async def fetch_html_aiohttp(
    session: aiohttp.ClientSession,
    url: str,
    rotator: RequestRotator,
) -> str:
    headers = {
        "User-Agent": rotator.pick_user_agent(),
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
    }
    proxy = rotator.pick_proxy()
    async with session.get(url, headers=headers, proxy=proxy) as response:
        response.raise_for_status()
        return await response.text()


async def fetch_html_playwright(url: str, user_agent: str) -> str:
    try:
        from playwright.async_api import async_playwright
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("playwright is not installed") from exc

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent=user_agent)
        await page.goto(url, wait_until="networkidle", timeout=45000)
        await asyncio.sleep(1.0)
        content = await page.content()
        await browser.close()
        return content
