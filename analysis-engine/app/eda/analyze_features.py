from __future__ import annotations

import pandas as pd

from app.db.postgres import get_connection


FEATURE_COLUMNS = [
    "num_attempts",
    "session_duration",
    "auth_failure_ratio",
    "unique_users",
    "mean_dt",
    "std_dt",
    "burst_rate",
    "temporal_entropy",
    "transition_auth_to_command_ratio",
]


def load_data() -> pd.DataFrame:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    num_attempts,
                    session_duration,
                    auth_failure_ratio,
                    unique_users,
                    mean_dt,
                    std_dt,
                    burst_rate,
                    temporal_entropy,
                    transition_auth_to_command_ratio
                FROM session_features
                """
            )
            rows = cur.fetchall()

    df = pd.DataFrame(rows, columns=FEATURE_COLUMNS)

    for col in FEATURE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def main() -> None:
    df = load_data()

    print("\n=== BASIC INFO ===")
    print(df.info())

    print("\n=== DESCRIBE ===")
    print(df.describe())

    print("\n=== CORRELATION MATRIX ===")
    print(df.corr(numeric_only=True))

    print("\n=== FEATURE VARIANCE ===")
    print(df.var(numeric_only=True))

    print("\n=== UNIQUE VALUES ===")
    for col in df.columns:
        print(f"{col}: {df[col].nunique()} unique values")


if __name__ == "__main__":
    main()