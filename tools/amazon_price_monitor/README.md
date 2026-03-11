# Amazon Price Monitor (asyncio + aiohttp)

Features:
- async fetch loop with `aiohttp`
- URL list loaded from file
- price/title extraction with `BeautifulSoup`
- threshold alerts to Telegram bot
- User-Agent rotation and proxy rotation
- dynamic-content fallback with Playwright for JS-rendered pages

## Setup
```bash
pip install aiohttp beautifulsoup4 playwright
playwright install chromium
```

## Run
```bash
python -m tools.amazon_price_monitor.main --config tools/amazon_price_monitor/config.example.json --urls tools/amazon_price_monitor/urls.example.txt
```

## Notes
- For Amazon pages, selectors and anti-bot behavior can change; rotate UAs/proxies responsibly.
- Telegram alert is sent when price crosses below threshold compared to previous observed value.
