from __future__ import annotations

import base64
import json
import random
import socket
from dataclasses import dataclass

MAX_DATAGRAM = 64 * 1024


@dataclass
class Segment:
    type: str
    seq: int = 0
    ack: int = 0
    payload: bytes = b""
    filename: str = ""
    total_size: int = 0

    def to_bytes(self) -> bytes:
        obj = {
            "type": self.type,
            "seq": self.seq,
            "ack": self.ack,
            "filename": self.filename,
            "total_size": self.total_size,
            "payload": base64.b64encode(self.payload).decode("ascii"),
        }
        return json.dumps(obj, separators=(",", ":")).encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> "Segment":
        obj = json.loads(data.decode("utf-8"))
        payload = base64.b64decode(obj.get("payload", ""))
        return cls(
            type=obj["type"],
            seq=int(obj.get("seq", 0)),
            ack=int(obj.get("ack", 0)),
            payload=payload,
            filename=obj.get("filename", ""),
            total_size=int(obj.get("total_size", 0)),
        )


class UnreliableSocket:
    def __init__(self, sock: socket.socket, drop_rate: float = 0.0) -> None:
        self.sock = sock
        self.drop_rate = max(0.0, min(1.0, drop_rate))

    def sendto(self, data: bytes, addr: tuple[str, int]) -> int:
        if random.random() < self.drop_rate:
            return len(data)
        return self.sock.sendto(data, addr)

    def recvfrom(self, bufsize: int = MAX_DATAGRAM) -> tuple[bytes, tuple[str, int]]:
        return self.sock.recvfrom(bufsize)
