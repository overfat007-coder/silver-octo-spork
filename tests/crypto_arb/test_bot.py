import asyncio

from tools.crypto_arb_bot.bot import PaperArbBot
from tools.crypto_arb_bot.models import OrderBookTop, utc_now


class InMemoryStore:
    def __init__(self) -> None:
        self.rows = []

    def insert(self, opp) -> None:
        self.rows.append(opp)


def test_bot_logs_when_opportunity_exists() -> None:
    store = InMemoryStore()
    bot = PaperArbBot(
        symbol="BTC/USDT",
        store=store,
        notional_usdt=1000,
        taker_fee_buy_pct=0.1,
        taker_fee_sell_pct=0.1,
        transfer_cost_pct=0.05,
        min_spread_pct=0.2,
    )

    bot.last_books["binance"] = OrderBookTop("binance", "BTC/USDT", bid=100.0, ask=99.0, ts=utc_now())
    bot.last_books["bybit"] = OrderBookTop("bybit", "BTC/USDT", bid=101.0, ask=101.5, ts=utc_now())

    asyncio.run(bot._evaluate_and_log())
    assert len(store.rows) == 1
