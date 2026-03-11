from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass

from tools.blockchain_vote.crypto import RSAPublicKey, rsa_verify


@dataclass
class VoteTransaction:
    voter_public_n: int
    voter_public_e: int
    candidate: str
    voter_signature: int
    authority_signature: int
    timestamp: float

    def signing_payload(self) -> str:
        return f"{self.candidate}:{self.timestamp:.6f}"

    def authority_payload(self) -> str:
        return self.candidate


@dataclass
class Block:
    index: int
    prev_hash: str
    timestamp: float
    votes: list[VoteTransaction]
    proposer: str

    def block_hash(self) -> str:
        payload = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "proposer": self.proposer,
            "votes": [asdict(v) for v in self.votes],
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class VotingBlockchain:
    def __init__(self, authority_pubkey: RSAPublicKey) -> None:
        self.authority_pubkey = authority_pubkey
        self.pending_votes: list[VoteTransaction] = []
        self.chain: list[Block] = [
            Block(index=0, prev_hash="0" * 64, timestamp=time.time(), votes=[], proposer="genesis")
        ]
        self.seen_signatures: set[int] = set()

    def add_vote(self, vote: VoteTransaction) -> bool:
        if vote.voter_signature in self.seen_signatures:
            return False
        if not self._validate_vote(vote):
            return False
        self.pending_votes.append(vote)
        self.seen_signatures.add(vote.voter_signature)
        return True

    def build_candidate_block(self, proposer: str) -> Block | None:
        if not self.pending_votes:
            return None
        return Block(
            index=len(self.chain),
            prev_hash=self.chain[-1].block_hash(),
            timestamp=time.time(),
            votes=list(self.pending_votes),
            proposer=proposer,
        )

    def append_block(self, block: Block) -> bool:
        if not self.validate_block(block):
            return False
        self.chain.append(block)
        self.pending_votes = []
        return True

    def validate_block(self, block: Block) -> bool:
        prev = self.chain[-1]
        if block.index != prev.index + 1:
            return False
        if block.prev_hash != prev.block_hash():
            return False
        return all(self._validate_vote(v) for v in block.votes)

    def _validate_vote(self, vote: VoteTransaction) -> bool:
        voter_pub = RSAPublicKey(n=vote.voter_public_n, e=vote.voter_public_e)
        voter_ok = rsa_verify(vote.signing_payload(), vote.voter_signature, voter_pub)
        authority_ok = rsa_verify(vote.authority_payload(), vote.authority_signature, self.authority_pubkey)
        return voter_ok and authority_ok

    def to_dict(self) -> dict:
        return {
            "chain": [
                {
                    "index": b.index,
                    "prev_hash": b.prev_hash,
                    "timestamp": b.timestamp,
                    "proposer": b.proposer,
                    "votes": [asdict(v) for v in b.votes],
                    "hash": b.block_hash(),
                }
                for b in self.chain
            ],
            "pending_votes": [asdict(v) for v in self.pending_votes],
        }
