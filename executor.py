from llm import generate_sql
from prompt_builder import build_prompt, build_error_correction_prompt
from db import execute_query

MAX_RETRIES = 4


def _clean(sql):
    sql = sql.replace("```sql", "").replace("```", "").strip()
    lower = sql.lower()
    if "select" in lower:
        sql = sql[lower.index("select"):]
    if ";" in sql:
        sql = sql.split(";")[0].strip()
    return sql.strip()


def _is_select(sql):
    return sql.strip().lower().startswith("select")


def execute_with_retry(session_id, schema, question, api_key=None):
    # Allow direct SQL execution from the UI editor
    if question.startswith("RUN_RAW_SQL:"):
        sql = question[len("RUN_RAW_SQL:"):].strip()
        columns, result = execute_query(session_id, sql)
        if columns is not None:
            return (columns, result), sql, None
        return None, sql, result

    prompt = build_prompt(schema, question)
    sql = generate_sql(prompt, api_key)

    if sql.startswith("LLM_ERROR"):
        return None, sql, sql

    sql = _clean(sql)

    last_error = None
    for attempt in range(MAX_RETRIES):
        if not _is_select(sql):
            return None, sql, "Generated query is not a SELECT statement. Try rephrasing."

        columns, result = execute_query(session_id, sql)

        if columns is not None:
            return (columns, result), sql, None

        last_error = result
        fix_prompt = build_error_correction_prompt(schema, sql, result)
        sql = generate_sql(fix_prompt, api_key)

        if sql.startswith("LLM_ERROR"):
            return None, sql, sql

        sql = _clean(sql)

    return None, sql, f"Could not generate a working query after {MAX_RETRIES} attempts. Last error: {last_error}"
