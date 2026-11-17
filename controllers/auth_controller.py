"""AuthController: exchange credentials for a signed access token."""
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

import config
from db import get_db
from tokens import create_access_token

bp = Blueprint("auth", __name__, url_prefix="/api")


@bp.post("/login")
def login():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}
    username = payload.get("username")
    password = payload.get("password")
    if not isinstance(username, str) or not isinstance(password, str) or not username or not password:
        return jsonify(error="username and password are required"), 400

    user = get_db().execute(
        "SELECT id, username, password_hash, role, is_admin FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify(error="Invalid credentials"), 401

    return jsonify(
        access_token=create_access_token(user),
        token_type="Bearer",
        expires_in=config.JWT_EXPIRY_MINUTES * 60,
    )
