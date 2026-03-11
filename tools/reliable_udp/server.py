from __future__ import annotations

import socket
from pathlib import Path

from tools.reliable_udp.protocol import Segment, UnreliableSocket


class ReliableUDPServer:
    def __init__(self, host: str, port: int, output_dir: str, drop_rate: float = 0.0) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        sock.settimeout(10.0)
        self.usock = UnreliableSocket(sock, drop_rate=drop_rate)

    def close(self) -> None:
        self.usock.sock.close()

    def receive_one_file(self) -> Path:
        peer: tuple[str, int] | None = None
        filename = "received.bin"
        total_size = 0
        buffer: dict[int, bytes] = {}
        expected = 0

        while True:
            raw, addr = self.usock.recvfrom()
            seg = Segment.from_bytes(raw)
            peer = addr

            if seg.type == "META":
                filename = seg.filename or filename
                total_size = seg.total_size
                self.usock.sendto(Segment(type="META_ACK").to_bytes(), addr)
                continue

            if seg.type == "DATA":
                if seg.seq not in buffer:
                    buffer[seg.seq] = seg.payload
                while expected in buffer:
                    expected += 1
                self.usock.sendto(Segment(type="ACK", ack=expected - 1).to_bytes(), addr)
                continue

            if seg.type == "FIN":
                if peer:
                    self.usock.sendto(Segment(type="ACK", ack=expected - 1).to_bytes(), peer)
                break

        out = self.output_dir / filename
        with out.open("wb") as f:
            written = 0
            idx = 0
            while idx in buffer and (total_size == 0 or written < total_size):
                chunk = buffer[idx]
                if total_size:
                    remain = total_size - written
                    chunk = chunk[:remain]
                f.write(chunk)
                written += len(chunk)
                idx += 1
        return out
