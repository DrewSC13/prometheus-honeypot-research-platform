from pathlib import Path

from app.db.postgres import get_connection


def main() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    sql_files = [
        repo_root / "analysis-engine" / "sql" / "001_init_events_raw.sql",
        repo_root / "analysis-engine" / "sql" / "002_init_sessions.sql",
    ]

    with get_connection() as conn:
        with conn.cursor() as cur:
            for sql_file in sql_files:
                sql = sql_file.read_text(encoding="utf-8")
                cur.execute(sql)
        conn.commit()

    print("[OK] Database initialized successfully.")


if __name__ == "__main__":
    main()