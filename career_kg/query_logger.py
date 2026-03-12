"""
Career KG — Query Logger
SQLite-based logging for tracking HR recruiter queries.
"""
import sqlite3
import json
import os
from pathlib import Path
from contextlib import contextmanager


class QueryLogger:
    def __init__(self, db_path: str = None):
        if db_path is None:
            data_dir = Path(os.getenv("QUERY_LOG_DIR", Path(__file__).parent / "data"))
            data_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(data_dir / "query_logs.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_logs (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id  TEXT NOT NULL,
                    timestamp   TEXT DEFAULT (datetime('now')),
                    question    TEXT NOT NULL,
                    tool        TEXT,
                    parameters  TEXT,
                    answer      TEXT,
                    response_ms INTEGER,
                    user_agent  TEXT
                )
            """)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def log(self, session_id, question, tool, params, answer, response_ms, user_agent=""):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO query_logs (session_id, question, tool, parameters, answer, response_ms, user_agent) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    session_id,
                    question,
                    tool,
                    json.dumps(params, ensure_ascii=False),
                    answer[:500] if answer else "",
                    response_ms,
                    user_agent,
                ),
            )

    def get_recent(self, limit=50) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM query_logs ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    def get_stats(self) -> dict:
        with self._conn() as conn:
            total = conn.execute("SELECT COUNT(*) FROM query_logs").fetchone()[0]
            avg_ms = conn.execute("SELECT AVG(response_ms) FROM query_logs").fetchone()[0] or 0
            top_tools = conn.execute(
                "SELECT tool, COUNT(*) as cnt FROM query_logs "
                "GROUP BY tool ORDER BY cnt DESC LIMIT 5"
            ).fetchall()
            return {
                "total": total,
                "avg_ms": int(avg_ms),
                "top_tools": [{"tool": r[0], "count": r[1]} for r in top_tools],
            }
