"""Certificate generation and verification."""

import hashlib


def generate_certificate(user_id:str,course_id:str)->dict:
    token=hashlib.sha256(f'{user_id}:{course_id}'.encode()).hexdigest()
    return {'user_id':user_id,'course_id':course_id,'certificate_id':token[:16]}
