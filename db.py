import sqlite3
import pandas as pd
import os
import tempfile
import shutil

TEMP_DIR = os.path.join(tempfile.gettempdir(), "querymind_sessions")
os.makedirs(TEMP_DIR, exist_ok=True)


def _db_path(session_id):
    session_dir = os.path.join(TEMP_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, "data.db")


def _connect(session_id):
    return sqlite3.connect(_db_path(session_id))


def upload_dataframe(session_id, table_name, df):
    conn = _connect(session_id)
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.commit()
    finally:
        conn.close()


def get_tables(session_id):
    conn = _connect(session_id)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        result = []
        for (name,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM \"{name}\";")
            count = cursor.fetchone()[0]
            cursor.execute(f"PRAGMA table_info(\"{name}\");")
            cols = cursor.fetchall()
            result.append({
                "name": name,
                "rows": count,
                "columns": [c[1] for c in cols]
            })
        return result
    except Exception:
        return []
    finally:
        conn.close()


def get_schema(session_id):
    conn = _connect(session_id)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()

        if not tables:
            return ""

        schema_parts = []
        for (table_name,) in tables:
            cursor.execute(f"PRAGMA table_info(\"{table_name}\");")
            columns = cursor.fetchall()

            col_lines = [f"  - {col[1]} ({col[2]})" for col in columns]
            col_names = [col[1] for col in columns]

            cursor.execute(f"SELECT * FROM \"{table_name}\" LIMIT 3;")
            sample_rows = cursor.fetchall()

            sample_lines = []
            for row in sample_rows:
                row_dict = dict(zip(col_names, row))
                sample_lines.append(f"    {row_dict}")

            part = f"Table: {table_name}\n" + "\n".join(col_lines)
            if sample_lines:
                part += "\n  Sample rows:\n" + "\n".join(sample_lines)

            schema_parts.append(part)

        return "\n\n".join(schema_parts)

    except Exception as e:
        return str(e)
    finally:
        conn.close()


def execute_query(session_id, query):
    try:
        stripped = query.strip().lower()
        if not stripped.startswith("select"):
            return None, "Only SELECT queries are allowed."

        conn = _connect(session_id)
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
        finally:
            conn.close()

    except Exception as e:
        return None, str(e)


def delete_table(session_id, table_name):
    conn = _connect(session_id)
    try:
        conn.execute(f"DROP TABLE IF EXISTS \"{table_name}\";")
        conn.commit()
    finally:
        conn.close()


def clear_session(session_id):
    session_dir = os.path.join(TEMP_DIR, session_id)
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
