import argparse
import asyncio
import json
import logging
from pathlib import Path

from tools.crypto_arb_bot.bot import PaperArbBot
from tools.crypto_arb_bot.storage import PostgresOpportunityStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Crypto arbitrage bot (paper trading)")
    parser.add_argument("--config", required=True, help="Path to JSON config")
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))

    store = PostgresOpportunityStore(config["postgres_dsn"])
    store.init_schema()

    bot = PaperArbBot(
        symbol=config.get("symbol", "BTC/USDT"),
        store=store,
        notional_usdt=float(config.get("notional_usdt", 1000)),
        taker_fee_buy_pct=float(config.get("taker_fee_buy_pct", 0.1)),
        taker_fee_sell_pct=float(config.get("taker_fee_sell_pct", 0.1)),
        transfer_cost_pct=float(config.get("transfer_cost_pct", 0.05)),
        min_spread_pct=float(config.get("min_spread_pct", 0.2)),
    )

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(bot.run_forever())


if __name__ == "__main__":
    main()
