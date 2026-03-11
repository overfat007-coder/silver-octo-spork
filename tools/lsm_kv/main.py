from __future__ import annotations

import argparse

from tools.lsm_kv.store import LSMKVStore


def repl(data_dir: str) -> None:
    store = LSMKVStore(data_dir=data_dir)
    print("LSM KV Store REPL. Commands: PUT k v | GET k | DELETE k | COMPACT | STATS | EXIT")
    try:
        while True:
            raw = input("lsm> ").strip()
            if not raw:
                continue
            parts = raw.split(maxsplit=2)
            cmd = parts[0].upper()

            if cmd == "PUT" and len(parts) == 3:
                key, value = parts[1], parts[2]
                store.put(key, value)
                print("OK")
            elif cmd == "GET" and len(parts) == 2:
                key = parts[1]
                val = store.get(key)
                print(val if val is not None else "(nil)")
            elif cmd == "DELETE" and len(parts) == 2:
                store.delete(parts[1])
                print("OK")
            elif cmd == "COMPACT":
                store.manual_compact()
                print("OK")
            elif cmd == "STATS":
                print(store.stats())
            elif cmd in {"EXIT", "QUIT"}:
                break
            else:
                print("Unknown command")
    finally:
        store.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Simplified LSM-tree KV store")
    parser.add_argument("--data-dir", default="./.lsm_data")
    args = parser.parse_args()
    repl(args.data_dir)


if __name__ == "__main__":
    main()
