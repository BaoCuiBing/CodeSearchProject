import hashlib
import secrets

def generate_salt() -> str:
    """生成密码盐"""
    return secrets.token_hex(32)

def hash_password(password: str, salt: str) -> str:
    """密码加密"""
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def verify_password(password: str, salt: str, hashed_password: str) -> bool:
    """密码验证"""
    return hash_password(password, salt) == hashed_password
