from tools.crypto_arb_bot.models import ArbitrageOpportunity, OrderBookTop, utc_now


def evaluate_opportunity(
    book_a: OrderBookTop,
    book_b: OrderBookTop,
    notional_usdt: float,
    taker_fee_buy_pct: float,
    taker_fee_sell_pct: float,
    transfer_cost_pct: float,
    min_spread_pct: float,
) -> ArbitrageOpportunity | None:
    # Direction 1: buy A ask, sell B bid
    direction_candidates = [
        (book_a.exchange, book_a.ask, book_b.exchange, book_b.bid),
        (book_b.exchange, book_b.ask, book_a.exchange, book_a.bid),
    ]

    best = None
    for buy_ex, buy_px, sell_ex, sell_px in direction_candidates:
        gross_spread_pct = ((sell_px - buy_px) / buy_px) * 100
        total_cost_pct = taker_fee_buy_pct + taker_fee_sell_pct + transfer_cost_pct
        net_spread_pct = gross_spread_pct - total_cost_pct
        if best is None or net_spread_pct > best[0]:
            best = (net_spread_pct, buy_ex, buy_px, sell_ex, sell_px, gross_spread_pct)

    if best is None:
        return None

    net_spread_pct, buy_ex, buy_px, sell_ex, sell_px, gross_spread_pct = best
    if net_spread_pct < min_spread_pct:
        return None

    estimated_profit_usdt = notional_usdt * (net_spread_pct / 100)
    return ArbitrageOpportunity(
        symbol=book_a.symbol,
        buy_exchange=buy_ex,
        sell_exchange=sell_ex,
        buy_price=buy_px,
        sell_price=sell_px,
        gross_spread_pct=gross_spread_pct,
        net_spread_pct=net_spread_pct,
        estimated_profit_usdt=estimated_profit_usdt,
        ts=utc_now(),
    )
