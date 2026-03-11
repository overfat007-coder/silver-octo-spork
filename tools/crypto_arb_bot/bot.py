import asyncio
import logging

from tools.crypto_arb_bot.exchanges import multiplex_books
from tools.crypto_arb_bot.models import OrderBookTop
from tools.crypto_arb_bot.strategy import evaluate_opportunity

logger = logging.getLogger("crypto_arb_bot")


class PaperArbBot:
    def __init__(
        self,
        symbol: str,
        store,
        notional_usdt: float,
        taker_fee_buy_pct: float,
        taker_fee_sell_pct: float,
        transfer_cost_pct: float,
        min_spread_pct: float,
    ) -> None:
        self.symbol = symbol
        self.store = store
        self.notional_usdt = notional_usdt
        self.taker_fee_buy_pct = taker_fee_buy_pct
        self.taker_fee_sell_pct = taker_fee_sell_pct
        self.transfer_cost_pct = transfer_cost_pct
        self.min_spread_pct = min_spread_pct

        self.last_books: dict[str, OrderBookTop] = {}

    async def run_forever(self) -> None:
        q: asyncio.Queue[OrderBookTop] = asyncio.Queue()
        producer = asyncio.create_task(multiplex_books(self.symbol, q))
        try:
            while True:
                book = await q.get()
                self.last_books[book.exchange] = book
                if {"binance", "bybit"}.issubset(self.last_books):
                    await self._evaluate_and_log()
        finally:
            producer.cancel()

    async def _evaluate_and_log(self) -> None:
        opp = evaluate_opportunity(
            self.last_books["binance"],
            self.last_books["bybit"],
            notional_usdt=self.notional_usdt,
            taker_fee_buy_pct=self.taker_fee_buy_pct,
            taker_fee_sell_pct=self.taker_fee_sell_pct,
            transfer_cost_pct=self.transfer_cost_pct,
            min_spread_pct=self.min_spread_pct,
        )
        if not opp:
            return

        await asyncio.to_thread(self.store.insert, opp)
        logger.info(
            "opportunity %s buy=%s sell=%s net=%.4f%% profit=%.4f",
            opp.symbol,
            opp.buy_exchange,
            opp.sell_exchange,
            opp.net_spread_pct,
            opp.estimated_profit_usdt,
        )
