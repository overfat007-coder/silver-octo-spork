from tools.blockchain_vote.crypto import (
    blind_message,
    generate_rsa_keypair,
    rsa_verify,
    sign_blinded_message,
    unblind_signature,
)


def test_blind_signature_roundtrip() -> None:
    pub, priv = generate_rsa_keypair(bits=512)
    message = "Alice"

    blinded, r = blind_message(message, pub)
    blinded_sig = sign_blinded_message(blinded, priv)
    sig = unblind_signature(blinded_sig, r, pub)

    assert rsa_verify(message, sig, pub)
