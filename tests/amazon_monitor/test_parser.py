import pytest

bs4 = pytest.importorskip("bs4")

from tools.amazon_price_monitor.parser import extract_snapshot


def test_extract_snapshot_basic() -> None:
    html = """
    <html>
      <span id='productTitle'>Awesome Gadget</span>
      <span id='priceblock_ourprice'>$123.45</span>
    </html>
    """
    snap = extract_snapshot("https://example.com/p", html)
    assert snap.title == "Awesome Gadget"
    assert snap.price == 123.45
    assert snap.currency == "$"
