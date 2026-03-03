"""Electronic signature helpers."""

import hashlib


def sign_payload(payload:str, signer:str)->str:
    return hashlib.sha256(f"{signer}:{payload}".encode()).hexdigest()


def verify_signature(payload:str, signer:str, sig:str)->bool:
    return sign_payload(payload, signer)==sig
