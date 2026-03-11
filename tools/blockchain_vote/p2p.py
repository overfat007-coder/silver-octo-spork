from __future__ import annotations

import json
import socket
import threading
from dataclasses import asdict

from tools.blockchain_vote.blockchain import Block, VoteTransaction, VotingBlockchain


class P2PNode:
    def __init__(self, host: str, port: int, peers: list[tuple[str, int]], blockchain: VotingBlockchain, node_id: str) -> None:
        self.host = host
        self.port = port
        self.peers = peers
        self.blockchain = blockchain
        self.node_id = node_id
        self._running = False
        self._server_thread: threading.Thread | None = None

    def start(self) -> None:
        self._running = True
        self._server_thread = threading.Thread(target=self._serve, daemon=True)
        self._server_thread.start()

    def stop(self) -> None:
        self._running = False

    def broadcast_vote(self, vote: VoteTransaction) -> None:
        self.broadcast({"type": "vote", "vote": asdict(vote)})

    def propose_block_with_majority(self) -> bool:
        block = self.blockchain.build_candidate_block(self.node_id)
        if block is None:
            return False

        proposal = {
            "type": "validate_block",
            "block": {
                "index": block.index,
                "prev_hash": block.prev_hash,
                "timestamp": block.timestamp,
                "proposer": block.proposer,
                "votes": [asdict(v) for v in block.votes],
            },
        }

        approvals = 1  # self vote
        total = 1 + len(self.peers)
        for peer in self.peers:
            resp = self.send(peer, proposal)
            if resp and resp.get("approved"):
                approvals += 1

        if approvals > total // 2:
            if self.blockchain.append_block(block):
                self.broadcast({"type": "new_block", "block": proposal["block"]})
                return True
        return False

    def broadcast(self, payload: dict) -> None:
        for peer in self.peers:
            self.send(peer, payload)

    def send(self, peer: tuple[str, int], payload: dict) -> dict | None:
        try:
            with socket.create_connection(peer, timeout=1.5) as conn:
                conn.sendall((json.dumps(payload) + "\n").encode("utf-8"))
                conn.settimeout(1.5)
                data = conn.recv(65536)
                if not data:
                    return None
                return json.loads(data.decode("utf-8"))
        except OSError:
            return None

    def _serve(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((self.host, self.port))
            srv.listen()
            srv.settimeout(1.0)
            while self._running:
                try:
                    conn, _ = srv.accept()
                except socket.timeout:
                    continue
                threading.Thread(target=self._handle_connection, args=(conn,), daemon=True).start()

    def _handle_connection(self, conn: socket.socket) -> None:
        with conn:
            raw = conn.recv(65536)
            if not raw:
                return
            try:
                payload = json.loads(raw.decode("utf-8").strip())
            except json.JSONDecodeError:
                conn.sendall(b'{"ok": false}')
                return

            msg_type = payload.get("type")
            if msg_type == "vote":
                vote = VoteTransaction(**payload["vote"])
                ok = self.blockchain.add_vote(vote)
                conn.sendall(json.dumps({"ok": ok}).encode("utf-8"))
                return

            if msg_type == "validate_block":
                blk = payload["block"]
                block = Block(
                    index=blk["index"],
                    prev_hash=blk["prev_hash"],
                    timestamp=blk["timestamp"],
                    proposer=blk["proposer"],
                    votes=[VoteTransaction(**v) for v in blk["votes"]],
                )
                conn.sendall(json.dumps({"approved": self.blockchain.validate_block(block)}).encode("utf-8"))
                return

            if msg_type == "new_block":
                blk = payload["block"]
                block = Block(
                    index=blk["index"],
                    prev_hash=blk["prev_hash"],
                    timestamp=blk["timestamp"],
                    proposer=blk["proposer"],
                    votes=[VoteTransaction(**v) for v in blk["votes"]],
                )
                ok = self.blockchain.append_block(block)
                conn.sendall(json.dumps({"ok": ok}).encode("utf-8"))
                return

            conn.sendall(json.dumps({"ok": False, "error": "unknown type"}).encode("utf-8"))
