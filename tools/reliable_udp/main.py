from __future__ import annotations

import argparse

from tools.reliable_udp.client import ReliableUDPClient
from tools.reliable_udp.server import ReliableUDPServer


def main() -> None:
    parser = argparse.ArgumentParser(description="Reliable UDP mini-TCP demo")
    sub = parser.add_subparsers(dest="mode", required=True)

    srv = sub.add_parser("server")
    srv.add_argument("--host", default="127.0.0.1")
    srv.add_argument("--port", type=int, default=9200)
    srv.add_argument("--output-dir", default="./received")
    srv.add_argument("--drop-rate", type=float, default=0.0)

    cli = sub.add_parser("client")
    cli.add_argument("--host", default="127.0.0.1")
    cli.add_argument("--port", type=int, default=9200)
    cli.add_argument("--file", required=True)
    cli.add_argument("--drop-rate", type=float, default=0.0)

    args = parser.parse_args()

    if args.mode == "server":
        server = ReliableUDPServer(args.host, args.port, args.output_dir, drop_rate=args.drop_rate)
        try:
            out = server.receive_one_file()
            print(f"received: {out}")
        finally:
            server.close()
    else:
        client = ReliableUDPClient(args.host, args.port, drop_rate=args.drop_rate)
        try:
            client.send_file(args.file)
            print("sent")
        finally:
            client.close()


if __name__ == "__main__":
    main()
