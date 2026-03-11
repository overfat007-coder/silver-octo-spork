import argparse
import asyncio
import logging

from tools.amazon_price_monitor.monitor import run_from_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Amazon price monitor")
    parser.add_argument("--config", required=True, help="Path to JSON config")
    parser.add_argument("--urls", required=True, help="Path to urls file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(run_from_files(args.config, args.urls))


if __name__ == "__main__":
    main()
