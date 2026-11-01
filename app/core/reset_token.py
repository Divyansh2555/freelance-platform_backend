import hashlib
import secrets


def create_reset_token():
    """
    Returns:
        token       -> user ko bhejne wala raw token
        token_hash  -> database me store hone wala hash
    """

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    return token, token_hash


def hash_reset_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()