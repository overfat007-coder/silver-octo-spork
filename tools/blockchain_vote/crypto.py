from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from math import gcd


def _is_probable_prime(n: int, rounds: int = 8) -> bool:
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _generate_prime(bits: int) -> int:
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if _is_probable_prime(candidate):
            return candidate


def _mod_inverse(a: int, m: int) -> int:
    t, new_t = 0, 1
    r, new_r = m, a
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r != 1:
        raise ValueError("inverse does not exist")
    if t < 0:
        t += m
    return t


@dataclass(frozen=True)
class RSAPublicKey:
    n: int
    e: int


@dataclass(frozen=True)
class RSAPrivateKey:
    n: int
    d: int


def generate_rsa_keypair(bits: int = 1024) -> tuple[RSAPublicKey, RSAPrivateKey]:
    e = 65537
    p = _generate_prime(bits // 2)
    q = _generate_prime(bits // 2)
    while q == p:
        q = _generate_prime(bits // 2)

    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        return generate_rsa_keypair(bits)
    d = _mod_inverse(e, phi)
    return RSAPublicKey(n=n, e=e), RSAPrivateKey(n=n, d=d)


def hash_to_int(message: str, n: int) -> int:
    digest = hashlib.sha256(message.encode("utf-8")).digest()
    return int.from_bytes(digest, "big") % n


def rsa_sign(message: str, private_key: RSAPrivateKey) -> int:
    m = hash_to_int(message, private_key.n)
    return pow(m, private_key.d, private_key.n)


def rsa_verify(message: str, signature: int, public_key: RSAPublicKey) -> bool:
    expected = hash_to_int(message, public_key.n)
    return pow(signature, public_key.e, public_key.n) == expected


def blind_message(message: str, public_key: RSAPublicKey) -> tuple[int, int]:
    m = hash_to_int(message, public_key.n)
    while True:
        r = secrets.randbelow(public_key.n - 2) + 2
        if gcd(r, public_key.n) == 1:
            break
    blinded = (m * pow(r, public_key.e, public_key.n)) % public_key.n
    return blinded, r


def sign_blinded_message(blinded_message: int, private_key: RSAPrivateKey) -> int:
    return pow(blinded_message, private_key.d, private_key.n)


def unblind_signature(blinded_signature: int, r: int, public_key: RSAPublicKey) -> int:
    r_inv = _mod_inverse(r, public_key.n)
    return (blinded_signature * r_inv) % public_key.n
