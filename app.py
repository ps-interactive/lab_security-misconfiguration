"""Globomantics User Management API."""
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

import config
import db
from controllers import admin_controller, auth_controller, user_controller


def create_app() -> Flask:
    if not config.DATABASE_PATH.exists():
        raise RuntimeError("Database not found. Run `python seed.py` first.")

    app = Flask(__name__)
    app.teardown_appcontext(db.close_db)

    for controller in (auth_controller, user_controller, admin_controller):
        app.register_blueprint(controller.bp)

    @app.errorhandler(Exception)
    def handle_error(error):
        # Always answer in JSON and never leak stack traces to clients.
        if isinstance(error, HTTPException):
            return jsonify(error=error.name), error.code
        app.logger.exception("Unhandled error")
        return jsonify(error="Internal Server Error"), 500

    return app


if __name__ == "__main__":
    # debug=False on purpose: Flask's debugger allows remote code execution.
    # The reloader restarts the server automatically when you save a file.
    create_app().run(host="127.0.0.1", port=5000, debug=False, use_reloader=True)
