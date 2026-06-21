import sqlite3
import os
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(__file__), "analytics.db")


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id   TEXT PRIMARY KEY,
            ip           TEXT,
            first_seen   TEXT,
            last_active  TEXT,
            query_count  INTEGER DEFAULT 0,
            tables_uploaded TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS queries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  TEXT,
            question    TEXT,
            sql_out     TEXT,
            success     INTEGER,
            used_own_key INTEGER DEFAULT 0,
            ts          TEXT
        );
    """)
    conn.commit()
    conn.close()


def log_session(session_id, ip):
    conn = _conn()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO sessions (session_id, ip, first_seen, last_active, query_count)
        VALUES (?, ?, ?, ?, 0)
        ON CONFLICT(session_id) DO UPDATE SET last_active = excluded.last_active
    """, (session_id, ip, now, now))
    conn.commit()
    conn.close()


def log_query(session_id, question, sql_out, success, used_own_key=False):
    conn = _conn()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("""
        INSERT INTO queries (session_id, question, sql_out, success, used_own_key, ts)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, question, sql_out, 1 if success else 0, 1 if used_own_key else 0, now))
    conn.execute("""
        UPDATE sessions SET query_count = query_count + 1, last_active = ?
        WHERE session_id = ?
    """, (now, session_id))
    conn.commit()
    conn.close()


def log_table_upload(session_id, table_name):
    conn = _conn()
    row = conn.execute("SELECT tables_uploaded FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
    if row:
        existing = row["tables_uploaded"] or ""
        tables = [t for t in existing.split(",") if t]
        if table_name not in tables:
            tables.append(table_name)
        conn.execute("UPDATE sessions SET tables_uploaded = ? WHERE session_id = ?",
                     (",".join(tables), session_id))
        conn.commit()
    conn.close()


def get_stats():
    conn = _conn()
    today = date.today().strftime("%Y-%m-%d")

    total_sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    sessions_today = conn.execute("SELECT COUNT(*) FROM sessions WHERE first_seen LIKE ?", (today + "%",)).fetchone()[0]
    total_queries  = conn.execute("SELECT COUNT(*) FROM queries").fetchone()[0]
    queries_today  = conn.execute("SELECT COUNT(*) FROM queries WHERE ts LIKE ?", (today + "%",)).fetchone()[0]
    own_key_users  = conn.execute("SELECT COUNT(DISTINCT session_id) FROM queries WHERE used_own_key = 1").fetchone()[0]

    sessions = conn.execute("""
        SELECT session_id, ip, first_seen, last_active, query_count, tables_uploaded
        FROM sessions ORDER BY last_active DESC LIMIT 50
    """).fetchall()

    recent_queries = conn.execute("""
        SELECT q.ts, q.session_id, q.question, q.sql_out, q.success, q.used_own_key
        FROM queries q ORDER BY q.id DESC LIMIT 30
    """).fetchall()

    conn.close()

    return {
        "total_sessions":  total_sessions,
        "sessions_today":  sessions_today,
        "total_queries":   total_queries,
        "queries_today":   queries_today,
        "own_key_users":   own_key_users,
        "sessions":        [dict(r) for r in sessions],
        "recent_queries":  [dict(r) for r in recent_queries],
    }
