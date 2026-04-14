from __future__ import annotations

import json
from typing import Any

from app.db.postgres import get_connection


FP_VERSION = "fingerprint_v1"


def fetch_feature_rows() -> list[dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    session_id,
                    num_attempts,
                    session_duration,
                    auth_failure_ratio,
                    unique_users,
                    mean_dt,
                    std_dt,
                    burst_rate,
                    temporal_entropy,
                    transition_auth_to_command_ratio,
                    feature_version
                FROM session_features
                ORDER BY created_at DESC
                """
            )
            return cur.fetchall()


def build_fp_vector(row: dict[str, Any]) -> list[float]:
    return [
        float(row["num_attempts"]),
        float(row["session_duration"]),
        float(row["unique_users"]),
        float(row["auth_failure_ratio"]),
        float(row["mean_dt"]),
        float(row["std_dt"]),
        float(row["burst_rate"]),
        float(row["temporal_entropy"]),
        float(row["transition_auth_to_command_ratio"]),
    ]


def assign_fingerprint_label(row: dict[str, Any]) -> str:
    num_attempts = float(row["num_attempts"])
    session_duration = float(row["session_duration"])
    auth_failure_ratio = float(row["auth_failure_ratio"])
    mean_dt = float(row["mean_dt"])
    burst_rate = float(row["burst_rate"])

    if num_attempts == 0 and session_duration == 0:
        return "single_touch_session"

    if num_attempts >= 1 and auth_failure_ratio == 1.0 and burst_rate >= 0.7:
        return "repeated_auth_probe"

    if num_attempts >= 1 and auth_failure_ratio == 1.0 and mean_dt >= 5.0:
        return "slow_probe_like"

    if num_attempts >= 1 and auth_failure_ratio == 1.0:
        return "failed_auth_session"

    return "unknown_pattern"


def persist_fingerprint(session_id: str, fp_vector: list[float], label: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE session_features
                SET
                    fp_vector = %s::jsonb,
                    fingerprint_label = %s
                WHERE session_id = %s
                """,
                (
                    json.dumps(
                        {
                            "fp_version": FP_VERSION,
                            "vector": fp_vector,
                        }
                    ),
                    label,
                    session_id,
                ),
            )
        conn.commit()


def main() -> None:
    rows = fetch_feature_rows()
    print(f"[INFO] fetched {len(rows)} session feature rows")

    for row in rows:
        session_id = str(row["session_id"])
        fp_vector = build_fp_vector(row)
        label = assign_fingerprint_label(row)

        persist_fingerprint(session_id, fp_vector, label)

        print(
            f"[OK] fingerprinted session_id={session_id} "
            f"label={label} "
            f"fp_vector={fp_vector}"
        )

    print("[OK] Fingerprinting v1 completed successfully.")


if __name__ == "__main__":
    main()