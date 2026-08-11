import base64
import hashlib

import bcrypt


def pre_hash_password(password: str) -> bytes:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)

def hash_password(password: str) -> str:
    pre_hashed = pre_hash_password(password)
    return bcrypt.hashpw(pre_hashed, bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pre_hashed = pre_hash_password(plain_password)
    return bcrypt.checkpw(pre_hashed, hashed_password.encode("utf-8"))