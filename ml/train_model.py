"""Offline ML training placeholder script for TaskFeatures."""

from pathlib import Path


def main() -> None:
    Path("ml/model.pkl").write_bytes(b"placeholder-model")
    print("model saved to ml/model.pkl")


if __name__ == "__main__":
    main()
