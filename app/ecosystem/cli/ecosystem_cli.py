"""CLI for ecosystem maintenance commands."""

import argparse

from app.ecosystem.serializers.json_serializer import JsonSerializer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ecosystem-cli")
    parser.add_argument("command", choices=["ping", "json-echo"])
    parser.add_argument("--value", default="{}")
    args = parser.parse_args(argv)

    if args.command == "ping":
        print("pong")
        return 0

    serializer = JsonSerializer()
    print(serializer.dumps(serializer.loads(args.value)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
