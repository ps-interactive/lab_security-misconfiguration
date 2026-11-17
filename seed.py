"""Create or reset the lab database.

Run `python seed.py` for a clean slate at any time. It recreates the users
table and restores every seeded account, including any that were deleted.
The JWT signing key is generated once and kept between resets.
"""
import os
import secrets
import sqlite3
from contextlib import closing

from werkzeug.security import generate_password_hash

import config

ADMIN_PASSWORD = "AdminPass123"
USER_PASSWORD = "UserPass123"

# (id, username, password, role, is_admin)
USERS = [
    (1, "alice", ADMIN_PASSWORD, "admin", 1),
    (2, "bob", USER_PASSWORD, "user", 0),
    (3, "carol", USER_PASSWORD, "user", 0),
    (4, "dave", USER_PASSWORD, "user", 0),
    (5, "erin", USER_PASSWORD, "user", 0),
]

SCHEMA = """
CREATE TABLE users (
    id            INTEGER PRIMARY KEY,
    username      TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL CHECK (role IN ('user', 'admin')),
    is_admin      INTEGER NOT NULL DEFAULT 0 CHECK (is_admin IN (0, 1))
);
"""


def main() -> None:
    config.INSTANCE_DIR.mkdir(exist_ok=True)

    if not config.JWT_SECRET_PATH.exists():
        config.JWT_SECRET_PATH.write_text(secrets.token_hex(32), encoding="utf-8")
        os.chmod(config.JWT_SECRET_PATH, 0o600)

    with closing(sqlite3.connect(config.DATABASE_PATH)) as conn:
        conn.execute("DROP TABLE IF EXISTS users")
        conn.executescript(SCHEMA)
        conn.executemany(
            "INSERT INTO users (id, username, password_hash, role, is_admin) VALUES (?, ?, ?, ?, ?)",
            [(uid, name, generate_password_hash(pw), role, flag) for uid, name, pw, role, flag in USERS],
        )
        conn.commit()

    print(f"Database ready: {config.DATABASE_PATH}\n")
    print(f"{'id':<4}{'username':<10}{'password':<15}{'role':<7}is_admin")
    for uid, name, pw, role, flag in USERS:
        print(f"{uid:<4}{name:<10}{pw:<15}{role:<7}{flag}")


if __name__ == "__main__":
    main()
