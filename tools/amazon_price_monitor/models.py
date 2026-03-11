from dataclasses import dataclass


@dataclass
class ProductSnapshot:
    url: str
    title: str
    price: float
    currency: str


@dataclass
class MonitorState:
    last_price: float | None = None
