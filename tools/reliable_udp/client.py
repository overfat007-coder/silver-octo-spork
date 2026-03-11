from __future__ import annotations

import math
import os
import socket
import time

from tools.reliable_udp.protocol import Segment, UnreliableSocket


class ReliableUDPClient:
    def __init__(
        self,
        server_host: str,
        server_port: int,
        drop_rate: float = 0.0,
        chunk_size: int = 1024,
        timeout_s: float = 0.25,
    ) -> None:
        self.server_addr = (server_host, server_port)
        self.chunk_size = chunk_size
        self.timeout_s = timeout_s

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout_s)
        self.usock = UnreliableSocket(sock, drop_rate=drop_rate)

    def close(self) -> None:
        self.usock.sock.close()

    def send_file(self, filepath: str) -> None:
        with open(filepath, "rb") as f:
            data = f.read()

        filename = os.path.basename(filepath)
        total_size = len(data)
        total_segments = math.ceil(total_size / self.chunk_size)

        self._send_meta(filename, total_size)

        base = 0
        next_seq = 0
        unacked: dict[int, tuple[float, bytes]] = {}

        cwnd = 1.0
        ssthresh = 16.0
        dupacks = 0
        last_ack = -1

        while base < total_segments:
            window = max(1, int(cwnd))
            while next_seq < base + window and next_seq < total_segments:
                payload = data[next_seq * self.chunk_size : (next_seq + 1) * self.chunk_size]
                seg = Segment(type="DATA", seq=next_seq, payload=payload)
                self.usock.sendto(seg.to_bytes(), self.server_addr)
                unacked[next_seq] = (time.monotonic(), payload)
                next_seq += 1

            try:
                raw, _ = self.usock.recvfrom()
                ack = Segment.from_bytes(raw)
                if ack.type != "ACK":
                    continue
                ack_num = ack.ack
                if ack_num >= base:
                    for s in range(base, ack_num + 1):
                        unacked.pop(s, None)
                    base = ack_num + 1
                    if cwnd < ssthresh:
                        cwnd += 1.0
                    else:
                        cwnd += 1.0 / max(cwnd, 1.0)
                    dupacks = 0
                    last_ack = ack_num
                elif ack_num == last_ack:
                    dupacks += 1
                    if dupacks >= 3 and base in unacked:
                        ssthresh = max(cwnd / 2.0, 2.0)
                        cwnd = ssthresh + 3.0
                        self.usock.sendto(Segment(type="DATA", seq=base, payload=unacked[base][1]).to_bytes(), self.server_addr)
                        dupacks = 0
            except socket.timeout:
                if base in unacked:
                    ssthresh = max(cwnd / 2.0, 2.0)
                    cwnd = 1.0
                    self.usock.sendto(Segment(type="DATA", seq=base, payload=unacked[base][1]).to_bytes(), self.server_addr)

        self.usock.sendto(Segment(type="FIN", seq=total_segments).to_bytes(), self.server_addr)

    def _send_meta(self, filename: str, total_size: int) -> None:
        meta = Segment(type="META", filename=filename, total_size=total_size)
        while True:
            self.usock.sendto(meta.to_bytes(), self.server_addr)
            try:
                raw, _ = self.usock.recvfrom()
                ack = Segment.from_bytes(raw)
                if ack.type == "META_ACK":
                    return
            except socket.timeout:
                continue
