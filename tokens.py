"""Creation and verification of signed JWT access tokens."""
from datetime import datetime, timedelta, timezone

import jwt

import config


def create_access_token(user) -> str:
    """Issue a signed token carrying the user's identity and authorization claims."""
    now = datetime.now(timezone.utc)
    claims = {
        "sub": str(user["id"]),
        "username": user["username"],
        "role": user["role"],
        "is_admin": bool(user["is_admin"]),
        "iat": now,
        "exp": now + timedelta(minutes=config.JWT_EXPIRY_MINUTES),
    }
    return jwt.encode(claims, config.get_jwt_secret(), algorithm=config.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Verify the signature and expiry, then return the claims.

    Raises jwt.InvalidTokenError for any problem.
    """
    return jwt.decode(
        token,
        config.get_jwt_secret(),
        algorithms=[config.JWT_ALGORITHM],
        options={"require": ["exp", "sub"]},
    )
