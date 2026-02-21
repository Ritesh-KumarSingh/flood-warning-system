"""
Authentication Module — register, login, session management.
Uses hashlib + random salt for password hashing (no extra deps).
"""

import hashlib
import os
import secrets
from typing import Dict, Optional, Tuple

import database as db


# ─── Password utilities ─────────────────────────────────────────────────────

def _hash_password(password: str, salt: str) -> str:
    """SHA-256 hash with salt."""
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def _make_salt() -> str:
    return secrets.token_hex(16)


# ─── Public API ──────────────────────────────────────────────────────────────

def register(username: str, email: str, password: str,
             full_name: str = "") -> Tuple[bool, str]:
    """
    Register a new user.
    Returns (success: bool, message: str).
    """
    # Basic validation
    username = username.strip()
    email = email.strip().lower()

    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    salt = _make_salt()
    pw_hash = _hash_password(password, salt)

    user_id = db.create_user(username, email, pw_hash, salt, full_name)
    if user_id is None:
        return False, "Username or email already exists."

    return True, f"Account created successfully! Welcome, {username}."


def login(username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
    """
    Authenticate a user.
    Returns (success, message, user_dict | None).
    """
    username = username.strip()
    user = db.get_user_by_username(username)

    if user is None:
        return False, "Invalid username or password.", None

    pw_hash = _hash_password(password, user["salt"])
    if pw_hash != user["password_hash"]:
        return False, "Invalid username or password.", None

    db.update_last_login(user["id"])

    # Return safe user info (no password / salt)
    safe_user = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "default_city": user["default_city"],
        "created_at": user["created_at"],
    }
    return True, f"Welcome back, {user['username']}!", safe_user


def is_logged_in(session_state) -> bool:
    """Check if a user is logged in via Streamlit session state."""
    return session_state.get("user") is not None


def get_current_user(session_state) -> Optional[Dict]:
    """Return the currently logged-in user dict, or None."""
    return session_state.get("user")


def logout(session_state):
    """Clear user from session state."""
    session_state.pop("user", None)
