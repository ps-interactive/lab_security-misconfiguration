"""Authentication middleware: proves who the caller is."""
from functools import wraps

import jwt
from flask import g, jsonify, request

from tokens import decode_access_token


def is_authenticated(view):
    """Require a valid Bearer token and expose its claims as g.user."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        scheme, _, token = request.headers.get("Authorization", "").partition(" ")
        if scheme.lower() != "bearer" or not token.strip():
            return jsonify(error="Authentication required"), 401

        try:
            claims = decode_access_token(token.strip())
            g.user = {
                "id": int(claims["sub"]),
                "username": claims.get("username"),
                "role": claims.get("role"),
                "is_admin": claims.get("is_admin") is True,
            }
        except (jwt.InvalidTokenError, ValueError):
            return jsonify(error="Invalid or expired token"), 401

        return view(*args, **kwargs)

    return wrapper
