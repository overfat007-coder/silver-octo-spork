from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class OrderBookTop:
    exchange: str
    symbol: str
    bid: float
    ask: float
    ts: datetime


@dataclass
class ArbitrageOpportunity:
    symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_price: float
    sell_price: float
    gross_spread_pct: float
    net_spread_pct: float
    estimated_profit_usdt: float
    ts: datetime


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)
