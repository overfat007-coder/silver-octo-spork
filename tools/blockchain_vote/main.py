from __future__ import annotations

import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from tools.blockchain_vote.blockchain import VoteTransaction, VotingBlockchain
from tools.blockchain_vote.crypto import (
    RSAPrivateKey,
    RSAPublicKey,
    blind_message,
    generate_rsa_keypair,
    rsa_sign,
    sign_blinded_message,
    unblind_signature,
)
from tools.blockchain_vote.p2p import P2PNode


class VotingService:
    def __init__(self, host: str, port: int, peers: list[tuple[str, int]]) -> None:
        self.host = host
        self.port = port
        self.authority_public, self.authority_private = generate_rsa_keypair(bits=1024)
        self.blockchain = VotingBlockchain(self.authority_public)
        self.node = P2PNode(host, port + 1000, peers, self.blockchain, node_id=f"{host}:{port+1000}")
        self.voter_keys: dict[str, tuple[RSAPublicKey, RSAPrivateKey]] = {}

    def start(self) -> None:
        self.node.start()

    def stop(self) -> None:
        self.node.stop()

    def submit_vote(self, voter_id: str, candidate: str) -> bool:
        if voter_id not in self.voter_keys:
            self.voter_keys[voter_id] = generate_rsa_keypair(bits=1024)
        voter_pub, voter_priv = self.voter_keys[voter_id]

        blinded, r = blind_message(candidate, self.authority_public)
        blind_signature = sign_blinded_message(blinded, self.authority_private)
        authority_signature = unblind_signature(blind_signature, r, self.authority_public)

        ts = time.time()
        payload = f"{candidate}:{ts:.6f}"
        vote = VoteTransaction(
            voter_public_n=voter_pub.n,
            voter_public_e=voter_pub.e,
            candidate=candidate,
            voter_signature=rsa_sign(payload, voter_priv),
            authority_signature=authority_signature,
            timestamp=ts,
        )
        accepted = self.blockchain.add_vote(vote)
        if accepted:
            self.node.broadcast_vote(vote)
        return accepted


class VotingHandler(BaseHTTPRequestHandler):
    service: VotingService | None = None

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/":
            self._send_html(self._index_page())
            return
        if self.path == "/api/chain":
            self._send_json(self.service.blockchain.to_dict() if self.service else {"error": "not initialized"})
            return
        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        form = parse_qs(raw)

        if self.path == "/vote":
            voter_id = form.get("voter_id", [""])[0].strip()
            candidate = form.get("candidate", [""])[0].strip()
            if self.service and voter_id and candidate:
                self.service.submit_vote(voter_id, candidate)
            self._redirect("/")
            return

        if self.path == "/api/propose":
            ok = self.service.node.propose_block_with_majority() if self.service else False
            self._send_json({"ok": ok})
            return

        self.send_error(404)

    def _index_page(self) -> str:
        return """
        <html><body>
        <h2>Учебное голосование (блокчейн)</h2>
        <form method='post' action='/vote'>
          <label>Voter ID: <input type='text' name='voter_id' required></label><br/><br/>
          <label>Candidate:
            <select name='candidate'>
              <option value='Alice'>Alice</option>
              <option value='Bob'>Bob</option>
              <option value='Charlie'>Charlie</option>
            </select>
          </label><br/><br/>
          <button type='submit'>Submit vote</button>
        </form>
        <p><a href='/api/chain'>View chain JSON</a></p>
        <form method='post' action='/api/propose'><button type='submit'>Propose block (majority validators)</button></form>
        </body></html>
        """

    def _send_html(self, content: str) -> None:
        body = content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, path: str) -> None:
        self.send_response(303)
        self.send_header("Location", path)
        self.end_headers()


def parse_peers(raw_peers: list[str]) -> list[tuple[str, int]]:
    peers: list[tuple[str, int]] = []
    for item in raw_peers:
        host, port = item.split(":", 1)
        peers.append((host, int(port)))
    return peers


def run_from_cli() -> None:
    parser = argparse.ArgumentParser(description="Educational blockchain voting node")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8100, help="HTTP port")
    parser.add_argument("--peer", action="append", default=[], help="P2P peer as host:port (P2P port)")
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()

    host = args.host
    port = args.port
    peers = parse_peers(args.peer)

    if args.config:
        cfg = json.loads(args.config.read_text())
        host = cfg.get("host", host)
        port = int(cfg.get("port", port))
        peers = parse_peers(cfg.get("peers", []))

    service = VotingService(host=host, port=port, peers=peers)
    service.start()
    VotingHandler.service = service

    server = HTTPServer((host, port), VotingHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        service.stop()
        server.server_close()


if __name__ == "__main__":
    run_from_cli()
