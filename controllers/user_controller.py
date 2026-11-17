"""UserController: basic profile lookups for logged-in users."""
from flask import Blueprint, jsonify

from db import get_db
from middleware.auth import is_authenticated

bp = Blueprint("users", __name__, url_prefix="/api/users")


@bp.get("/<username>")
@is_authenticated
def get_user(username):
    user = get_db().execute(
        "SELECT id, username, role FROM users WHERE username = ?", (username,)
    ).fetchone()
    if user is None:
        return jsonify(error="User not found"), 404
    return jsonify(dict(user))
