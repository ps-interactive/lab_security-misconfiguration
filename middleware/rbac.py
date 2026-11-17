from functools import wraps

from flask import g, jsonify


def authorize(role):
    raise NotImplementedError("TODO: implement authorize(role) in middleware/rbac.py")
