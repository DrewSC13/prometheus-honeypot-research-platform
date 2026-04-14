from __future__ import annotations

from typing import Any

import pandas as pd

from app.db.postgres import get_connection


REVIEW_FEATURES = [
    "num_attempts",
    "session_duration",
    "mean_dt",
    "std_dt",
    "burst_rate",
    "temporal_entropy",
]


def load_anomaly_review_data() -> pd.DataFrame:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    a.session_id,
                    a.anomaly_score,
                    a.is_anomalous,
                    a.model_version,
                    a.feature_set_version,
                    sf.fingerprint_label,
                    sf.num_attempts,
                    sf.session_duration,
                    sf.mean_dt,
                    sf.std_dt,
                    sf.burst_rate,
                    sf.temporal_entropy
                FROM anomalies a
                JOIN session_features sf
                    ON a.session_id = sf.session_id
                ORDER BY a.anomaly_score ASC
                """
            )
            rows = cur.fetchall()

    columns = [
        "session_id",
        "anomaly_score",
        "is_anomalous",
        "model_version",
        "feature_set_version",
        "fingerprint_label",
        "num_attempts",
        "session_duration",
        "mean_dt",
        "std_dt",
        "burst_rate",
        "temporal_entropy",
    ]

    df = pd.DataFrame(rows, columns=columns)

    numeric_cols = [
        "anomaly_score",
        "num_attempts",
        "session_duration",
        "mean_dt",
        "std_dt",
        "burst_rate",
        "temporal_entropy",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def compute_global_stats(df: pd.DataFrame) -> dict[str, dict[str, float]]:
    stats: dict[str, dict[str, float]] = {}

    for feature in REVIEW_FEATURES:
        mean_value = float(df[feature].mean())
        std_value = float(df[feature].std(ddof=0))

        # evitar división por cero
        if std_value == 0.0:
            std_value = 1.0

        stats[feature] = {
            "mean": mean_value,
            "std": std_value,
        }

    return stats


def describe_direction(value: float, mean_value: float) -> str:
    if value > mean_value:
        return "above baseline"
    if value < mean_value:
        return "below baseline"
    return "at baseline"


def explain_row(row: pd.Series, stats: dict[str, dict[str, float]], top_k: int = 3) -> list[tuple[str, float, str]]:
    deviations: list[tuple[str, float, str]] = []

    for feature in REVIEW_FEATURES:
        mean_value = stats[feature]["mean"]
        std_value = stats[feature]["std"]
        value = float(row[feature])

        z_like = abs((value - mean_value) / std_value)
        direction = describe_direction(value, mean_value)

        deviations.append((feature, z_like, direction))

    deviations.sort(key=lambda x: x[1], reverse=True)
    return deviations[:top_k]


def render_review(df: pd.DataFrame) -> None:
    stats = compute_global_stats(df)
    anomalous_df = df[df["is_anomalous"] == True].copy()

    print(f"[INFO] total sessions reviewed: {len(df)}")
    print(f"[INFO] anomalous sessions found: {len(anomalous_df)}")
    print()

    if anomalous_df.empty:
        print("[WARN] No anomalous sessions available for review.")
        return

    for _, row in anomalous_df.iterrows():
        explanations = explain_row(row, stats)

        print("=" * 80)
        print(f"session_id        : {row['session_id']}")
        print(f"anomaly_score     : {row['anomaly_score']:.6f}")
        print(f"fingerprint_label : {row['fingerprint_label']}")
        print(f"model_version     : {row['model_version']}")
        print(f"feature_set       : {row['feature_set_version']}")
        print("top drivers:")

        for feature, score, direction in explanations:
            print(
                f"  - {feature:<18} {direction:<15} "
                f"(deviation_score={score:.3f}, value={float(row[feature]):.3f}, mean={stats[feature]['mean']:.3f})"
            )

        print("summary:")
        print(
            f"  Session classified as anomalous with label '{row['fingerprint_label']}'. "
            f"Primary deviations suggest unusual temporal or structural behavior relative to the current baseline."
        )
        print()

    print("[OK] Anomaly review completed successfully.")


def main() -> None:
    df = load_anomaly_review_data()
    render_review(df)


if __name__ == "__main__":
    main()