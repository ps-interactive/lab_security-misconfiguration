"""AdminController: administrative actions on user accounts."""
from flask import Blueprint, jsonify

from db import get_db
from middleware.auth import is_authenticated

bp = Blueprint("admin", __name__, url_prefix="/api/users")


@bp.delete("/<username>")
@is_authenticated
def delete_user(username):
    db = get_db()
    result = db.execute("DELETE FROM users WHERE username = ?", (username,))
    db.commit()
    if result.rowcount == 0:
        return jsonify(error="User not found"), 404
    return jsonify(message=f"User '{username}' deleted", username=username)
