from app.db.postgres import init_db


def main() -> None:
    init_db()
    print("[OK] Database initialized successfully.")


if __name__ == "__main__":
    main()