"""Post-quantum security helpers with safe fallbacks.

If liboqs is unavailable, deterministic placeholders are used so the app remains runnable.
"""

import hashlib
import os
import secrets
import time


def qrng_seed(length: int = 32) -> bytes:
    entropy = os.urandom(length) + str(time.time_ns()).encode() + secrets.token_bytes(length)
    return hashlib.sha512(entropy).digest()[:length]


def sign_payload_post_quantum(payload: dict) -> dict:
    message = repr(sorted(payload.items())).encode()
    try:
        import oqs  # type: ignore

        with oqs.Signature("Dilithium2") as signer:
            public_key = signer.generate_keypair()
            signature = signer.sign(message)
            return {
                "algorithm": "Dilithium2",
                "public_key": public_key.hex(),
                "signature": signature.hex(),
            }
    except Exception:
        fake = hashlib.sha3_512(message + qrng_seed(16)).hexdigest()
        return {"algorithm": "fallback-sha3", "public_key": "", "signature": fake}


def pq_handshake_stub(user_id: int) -> dict:
    try:
        import oqs  # type: ignore

        with oqs.KeyEncapsulation("Kyber512") as kem:
            public_key = kem.generate_keypair()
            ciphertext, shared_secret = kem.encap_secret(public_key)
            return {
                "user_id": user_id,
                "kem": "Kyber512",
                "ciphertext": ciphertext.hex(),
                "shared_secret_preview": shared_secret.hex()[:32],
            }
    except Exception:
        return {
            "user_id": user_id,
            "kem": "fallback",
            "ciphertext": hashlib.sha256(qrng_seed(24)).hexdigest(),
            "shared_secret_preview": hashlib.sha256(qrng_seed(24)).hexdigest()[:32],
        }
