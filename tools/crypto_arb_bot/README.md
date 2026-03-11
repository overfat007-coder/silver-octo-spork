# Crypto Arbitrage Bot (Paper Trading)

Async bot that monitors Binance and Bybit order books via WebSocket and logs arbitrage opportunities.

## Features
- real-time top-of-book streams:
  - Binance `bookTicker`
  - Bybit spot orderbook
- spread evaluation with fees:
  - taker fee buy + taker fee sell + transfer cost
- risk filter:
  - ignore opportunities below `min_spread_pct`
- PostgreSQL logging of opportunities

## Run
```bash
python -m tools.crypto_arb_bot.main --config tools/crypto_arb_bot/config.example.json
```

## DB table
`arbitrage_opportunities` with fields:
- ts, symbol, buy_exchange, sell_exchange, buy_price, sell_price,
- gross_spread_pct, net_spread_pct, estimated_profit_usdt.
