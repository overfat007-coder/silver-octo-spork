from tools.crypto_arb_bot.models import OrderBookTop, utc_now
from tools.crypto_arb_bot.strategy import evaluate_opportunity


def test_spread_respects_risk_threshold() -> None:
    binance = OrderBookTop(exchange="binance", symbol="BTC/USDT", bid=100.0, ask=100.1, ts=utc_now())
    bybit = OrderBookTop(exchange="bybit", symbol="BTC/USDT", bid=100.3, ask=100.4, ts=utc_now())

    # High threshold should block
    assert (
        evaluate_opportunity(
            binance,
            bybit,
            notional_usdt=1000,
            taker_fee_buy_pct=0.1,
            taker_fee_sell_pct=0.1,
            transfer_cost_pct=0.05,
            min_spread_pct=1.0,
        )
        is None
    )


def test_spread_positive_when_above_threshold() -> None:
    binance = OrderBookTop(exchange="binance", symbol="BTC/USDT", bid=100.0, ask=99.0, ts=utc_now())
    bybit = OrderBookTop(exchange="bybit", symbol="BTC/USDT", bid=101.0, ask=101.5, ts=utc_now())

    opp = evaluate_opportunity(
        binance,
        bybit,
        notional_usdt=1000,
        taker_fee_buy_pct=0.1,
        taker_fee_sell_pct=0.1,
        transfer_cost_pct=0.05,
        min_spread_pct=0.2,
    )
    assert opp is not None
    assert opp.net_spread_pct > 0
