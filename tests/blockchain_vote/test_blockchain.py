import time

from tools.blockchain_vote.blockchain import VoteTransaction, VotingBlockchain
from tools.blockchain_vote.crypto import (
    blind_message,
    generate_rsa_keypair,
    rsa_sign,
    sign_blinded_message,
    unblind_signature,
)


def test_vote_and_block_append() -> None:
    authority_pub, authority_priv = generate_rsa_keypair(bits=512)
    voter_pub, voter_priv = generate_rsa_keypair(bits=512)
    chain = VotingBlockchain(authority_pub)

    candidate = "Bob"
    blinded, r = blind_message(candidate, authority_pub)
    blinded_sig = sign_blinded_message(blinded, authority_priv)
    authority_sig = unblind_signature(blinded_sig, r, authority_pub)

    ts = time.time()
    payload = f"{candidate}:{ts:.6f}"
    tx = VoteTransaction(
        voter_public_n=voter_pub.n,
        voter_public_e=voter_pub.e,
        candidate=candidate,
        voter_signature=rsa_sign(payload, voter_priv),
        authority_signature=authority_sig,
        timestamp=ts,
    )

    assert chain.add_vote(tx)
    block = chain.build_candidate_block("node-1")
    assert block is not None
    assert chain.append_block(block)
    assert len(chain.chain) == 2
    assert chain.chain[-1].votes[0].candidate == "Bob"
