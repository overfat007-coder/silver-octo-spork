import re

from bs4 import BeautifulSoup

from tools.amazon_price_monitor.models import ProductSnapshot


PRICE_SELECTORS = [
    "#priceblock_dealprice",
    "#priceblock_ourprice",
    "#priceblock_saleprice",
    "span.a-price span.a-offscreen",
    "span.a-price-whole",
]

TITLE_SELECTORS = ["#productTitle", "title"]


def _parse_price(raw: str) -> tuple[float, str]:
    text = raw.strip().replace("\xa0", " ")
    currency_match = re.search(r"[€$£¥₽]", text)
    currency = currency_match.group(0) if currency_match else "$"

    normalized = re.sub(r"[^0-9,\.]", "", text)
    if normalized.count(",") > 0 and normalized.count(".") > 0:
        if normalized.rfind(",") > normalized.rfind("."):
            normalized = normalized.replace(".", "").replace(",", ".")
        else:
            normalized = normalized.replace(",", "")
    elif normalized.count(",") > 0 and normalized.count(".") == 0:
        normalized = normalized.replace(",", ".")

    return float(normalized), currency


def extract_snapshot(url: str, html: str) -> ProductSnapshot:
    soup = BeautifulSoup(html, "html.parser")

    title = None
    for selector in TITLE_SELECTORS:
        node = soup.select_one(selector)
        if node and node.get_text(strip=True):
            title = node.get_text(strip=True)
            break

    price_text = None
    for selector in PRICE_SELECTORS:
        node = soup.select_one(selector)
        if node and node.get_text(strip=True):
            price_text = node.get_text(strip=True)
            break

    if not title:
        raise ValueError("title not found")
    if not price_text:
        raise ValueError("price not found")

    price, currency = _parse_price(price_text)
    return ProductSnapshot(url=url, title=title, price=price, currency=currency)
