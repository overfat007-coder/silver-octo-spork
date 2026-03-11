import psycopg2

from tools.crypto_arb_bot.models import ArbitrageOpportunity


class PostgresOpportunityStore:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def init_schema(self) -> None:
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS arbitrage_opportunities (
                        id SERIAL PRIMARY KEY,
                        ts TIMESTAMPTZ NOT NULL,
                        symbol TEXT NOT NULL,
                        buy_exchange TEXT NOT NULL,
                        sell_exchange TEXT NOT NULL,
                        buy_price DOUBLE PRECISION NOT NULL,
                        sell_price DOUBLE PRECISION NOT NULL,
                        gross_spread_pct DOUBLE PRECISION NOT NULL,
                        net_spread_pct DOUBLE PRECISION NOT NULL,
                        estimated_profit_usdt DOUBLE PRECISION NOT NULL
                    )
                    """
                )
            conn.commit()

    def insert(self, opp: ArbitrageOpportunity) -> None:
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO arbitrage_opportunities (
                        ts, symbol, buy_exchange, sell_exchange, buy_price, sell_price,
                        gross_spread_pct, net_spread_pct, estimated_profit_usdt
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        opp.ts,
                        opp.symbol,
                        opp.buy_exchange,
                        opp.sell_exchange,
                        opp.buy_price,
                        opp.sell_price,
                        opp.gross_spread_pct,
                        opp.net_spread_pct,
                        opp.estimated_profit_usdt,
                    ),
                )
            conn.commit()
