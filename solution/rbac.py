from functools import wraps

from flask import g, jsonify

ADMIN_ROLE = "admin"


def authorize(role):

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user = getattr(g, "user", None)
            if user is None:
                return jsonify(error="Authentication required"), 401

            if user.get("role") != role:
                return jsonify(error="Forbidden: insufficient privileges"), 403
            if role == ADMIN_ROLE and user.get("is_admin") is not True:
                return jsonify(error="Forbidden: insufficient privileges"), 403

            return view(*args, **kwargs)

        return wrapper

    return decorator
