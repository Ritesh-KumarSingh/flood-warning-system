"""
Database Manager — SQLite backend for the Disaster Warning Platform.
Stores users, risk check history, and community reports.
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional


_DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
DB_PATH = os.path.join(_DB_DIR, "disaster_app.db")


def _get_conn() -> sqlite3.Connection:
    """Return a connection with row-factory enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # dict-like access
    conn.execute("PRAGMA journal_mode=WAL")  # better concurrency
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT    UNIQUE NOT NULL,
            email           TEXT    UNIQUE NOT NULL,
            password_hash   TEXT    NOT NULL,
            salt            TEXT    NOT NULL,
            full_name       TEXT    DEFAULT '',
            default_city    TEXT    DEFAULT '',
            created_at      TEXT    NOT NULL,
            last_login      TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS risk_checks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL,
            city            TEXT    NOT NULL,
            disaster_type   TEXT    NOT NULL,
            risk_level      INTEGER NOT NULL,
            risk_label      TEXT    NOT NULL,
            confidence      REAL    DEFAULT 0,
            weather_summary TEXT    DEFAULT '',
            checked_at      TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS community_reports (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER,
            report_id       TEXT    UNIQUE NOT NULL,
            location        TEXT    NOT NULL,
            disaster_type   TEXT    NOT NULL,
            severity        TEXT    NOT NULL,
            description     TEXT    DEFAULT '',
            affected_count  INTEGER DEFAULT 0,
            needs_help      INTEGER DEFAULT 0,
            verified        INTEGER DEFAULT 0,
            upvotes         INTEGER DEFAULT 0,
            created_at      TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id             INTEGER PRIMARY KEY,
            phone               TEXT    DEFAULT '',
            blood_group         TEXT    DEFAULT '',
            medical_conditions  TEXT    DEFAULT '',
            address             TEXT    DEFAULT '',
            emergency_contact_name  TEXT DEFAULT '',
            emergency_contact_phone TEXT DEFAULT '',
            family_members      TEXT    DEFAULT '[]',
            default_city        TEXT    DEFAULT '',
            updated_at          TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialised:", DB_PATH)


# ─── User helpers ────────────────────────────────────────────────────────────

def create_user(username: str, email: str, password_hash: str, salt: str,
                full_name: str = "") -> Optional[int]:
    """Insert a new user. Returns user id or None on duplicate."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO users (username, email, password_hash, salt, full_name, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (username, email, password_hash, salt, full_name,
             datetime.now().isoformat())
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_username(username: str) -> Optional[Dict]:
    """Look up a user by username."""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM users WHERE username = ?",
                       (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_last_login(user_id: int):
    conn = _get_conn()
    conn.execute("UPDATE users SET last_login = ? WHERE id = ?",
                 (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()


# ─── Risk-check helpers ─────────────────────────────────────────────────────

def save_risk_check(user_id: int, city: str, disaster_type: str,
                    risk_level: int, risk_label: str,
                    confidence: float = 0, weather_summary: str = ""):
    """Persist a risk assessment result."""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO risk_checks "
        "(user_id, city, disaster_type, risk_level, risk_label, confidence, weather_summary, checked_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, city, disaster_type, risk_level, risk_label,
         confidence, weather_summary, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_risk_history(user_id: int, limit: int = 20) -> List[Dict]:
    """Return recent risk checks for a user."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM risk_checks WHERE user_id = ? ORDER BY checked_at DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── Community report helpers ────────────────────────────────────────────────

def save_community_report(report: Dict, user_id: Optional[int] = None):
    """Save a community report to the database."""
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO community_reports "
            "(user_id, report_id, location, disaster_type, severity, description, "
            "affected_count, needs_help, verified, upvotes, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, report['id'], report['location'], report['disaster_type'],
             report['severity'], report.get('description', ''),
             report.get('affected_count', 0),
             1 if report.get('needs_help') else 0,
             1 if report.get('verified') else 0,
             report.get('upvotes', 0),
             report.get('timestamp', datetime.now().isoformat()))
        )
        conn.commit()
    finally:
        conn.close()


def get_all_reports(limit: int = 50) -> List[Dict]:
    """Fetch recent community reports."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM community_reports ORDER BY created_at DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ─── User profile helpers ───────────────────────────────────────────────────

def get_profile(user_id: int) -> Optional[Dict]:
    """Return a user profile or None."""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM user_profiles WHERE user_id = ?",
                       (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def save_profile(user_id: int, data: Dict):
    """Insert or update a user profile."""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO user_profiles "
        "(user_id, phone, blood_group, medical_conditions, address, "
        " emergency_contact_name, emergency_contact_phone, family_members, default_city, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET "
        " phone=excluded.phone, blood_group=excluded.blood_group, "
        " medical_conditions=excluded.medical_conditions, address=excluded.address, "
        " emergency_contact_name=excluded.emergency_contact_name, "
        " emergency_contact_phone=excluded.emergency_contact_phone, "
        " family_members=excluded.family_members, default_city=excluded.default_city, "
        " updated_at=excluded.updated_at",
        (user_id,
         data.get('phone', ''),
         data.get('blood_group', ''),
         data.get('medical_conditions', ''),
         data.get('address', ''),
         data.get('emergency_contact_name', ''),
         data.get('emergency_contact_phone', ''),
         data.get('family_members', '[]'),
         data.get('default_city', ''),
         datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


# Auto-init on import
init_db()
