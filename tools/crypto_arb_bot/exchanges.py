import asyncio
import json

from tools.crypto_arb_bot.models import OrderBookTop, utc_now


async def binance_book_stream(symbol: str):
    stream_symbol = symbol.lower().replace("/", "")
    url = f"wss://stream.binance.com:9443/ws/{stream_symbol}@bookTicker"
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url, heartbeat=20) as ws:
            async for msg in ws:
                if msg.type != aiohttp.WSMsgType.TEXT:
                    continue
                payload = json.loads(msg.data)
                yield OrderBookTop(
                    exchange="binance",
                    symbol=symbol,
                    bid=float(payload["b"]),
                    ask=float(payload["a"]),
                    ts=utc_now(),
                )


async def bybit_book_stream(symbol: str):
    pair = symbol.replace("/", "")
    url = "wss://stream.bybit.com/v5/public/spot"
    sub = {"op": "subscribe", "args": [f"orderbook.1.{pair}"]}

    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url, heartbeat=20) as ws:
            await ws.send_json(sub)
            async for msg in ws:
                if msg.type != aiohttp.WSMsgType.TEXT:
                    continue
                payload = json.loads(msg.data)
                data = payload.get("data")
                if not data:
                    continue
                bids = data.get("b") or []
                asks = data.get("a") or []
                if not bids or not asks:
                    continue
                yield OrderBookTop(
                    exchange="bybit",
                    symbol=symbol,
                    bid=float(bids[0][0]),
                    ask=float(asks[0][0]),
                    ts=utc_now(),
                )


async def multiplex_books(symbol: str, out_queue: asyncio.Queue):
    async def pump(gen):
        async for item in gen:
            await out_queue.put(item)

    await asyncio.gather(
        pump(binance_book_stream(symbol)),
        pump(bybit_book_stream(symbol)),
    )
