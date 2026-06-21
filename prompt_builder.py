MAX_COLS_PER_TABLE = 40
MAX_SAMPLE_ROWS    = 2


def _truncate_schema(schema: str) -> str:
    """Limit columns per table to avoid token bloat on wide CSVs."""
    lines = schema.splitlines()
    result, col_count, in_sample = [], 0, False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Table:"):
            col_count, in_sample = 0, False
            result.append(line)
        elif stripped.startswith("- "):
            col_count += 1
            if col_count <= MAX_COLS_PER_TABLE:
                result.append(line)
            elif col_count == MAX_COLS_PER_TABLE + 1:
                result.append("  ... (additional columns truncated)")
        elif stripped == "Sample rows:":
            in_sample = True
            result.append(line)
        elif in_sample and stripped.startswith("{"):
            # keep only MAX_SAMPLE_ROWS sample rows
            sample_lines = [l for l in result if l.strip().startswith("{")]
            if len(sample_lines) < MAX_SAMPLE_ROWS:
                result.append(line)
        else:
            result.append(line)

    return "\n".join(result)


def build_prompt(schema, user_question):
    schema = _truncate_schema(schema)
    return f"""You are an expert SQLite SQL query generator.

DATABASE SCHEMA:
{schema}

STRICT RULES:
1. Use ONLY the tables and columns defined in the schema above.
2. Generate valid SQLite syntax only.
3. For string comparisons use LIKE for fuzzy matching when appropriate.
4. Return ONLY the raw SQL query — no explanation, no markdown fences, no backticks.
5. The query must start with SELECT.

USER QUESTION:
{user_question}

SQL:"""


def build_error_correction_prompt(schema, failed_query, error_message):
    schema = _truncate_schema(schema)
    return f"""You are an expert SQLite query fixer.

DATABASE SCHEMA:
{schema}

FAILED QUERY:
{failed_query}

ERROR:
{error_message}

Fix the query so it runs correctly on SQLite.
Return ONLY the corrected SQL — no explanation, no markdown, no backticks.

FIXED SQL:"""
