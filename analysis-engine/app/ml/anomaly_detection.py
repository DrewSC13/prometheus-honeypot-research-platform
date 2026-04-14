from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.db.postgres import get_connection


MODEL_VERSION = "isolation_forest_v1"
FEATURE_SET_VERSION = "feature_set_v2"

MODEL_FEATURES = [
    "num_attempts",
    "session_duration",
    "mean_dt",
    "std_dt",
    "burst_rate",
    "temporal_entropy",
]


def load_feature_data() -> pd.DataFrame:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                    session_id,
                    num_attempts,
                    session_duration,
                    mean_dt,
                    std_dt,
                    burst_rate,
                    temporal_entropy
                FROM session_features
                ORDER BY created_at DESC
                """
            )
            rows = cur.fetchall()

    df = pd.DataFrame(rows, columns=["session_id", *MODEL_FEATURES])

    for col in MODEL_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def build_pipeline(random_state: int = 42) -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "model",
                IsolationForest(
                    n_estimators=100,
                    contamination="auto",
                    random_state=random_state,
                ),
            ),
        ]
    )


def fit_and_score(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError("No session feature data available for anomaly detection.")

    X = df[MODEL_FEATURES].to_numpy(dtype=float)

    pipeline = build_pipeline()
    pipeline.fit(X)

    model = pipeline.named_steps["model"]
    anomaly_score = model.decision_function(pipeline.named_steps["scaler"].transform(X))
    predictions = model.predict(pipeline.named_steps["scaler"].transform(X))

    result_df = df.copy()
    result_df["anomaly_score"] = anomaly_score
    result_df["is_anomalous"] = predictions == -1

    return result_df


def persist_anomaly_results(df: pd.DataFrame) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            for _, row in df.iterrows():
                cur.execute(
                    """
                    INSERT INTO anomalies (
                        session_id,
                        anomaly_score,
                        is_anomalous,
                        model_version,
                        feature_set_version
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (session_id) DO UPDATE SET
                        anomaly_score = EXCLUDED.anomaly_score,
                        is_anomalous = EXCLUDED.is_anomalous,
                        model_version = EXCLUDED.model_version,
                        feature_set_version = EXCLUDED.feature_set_version
                    """,
                    (
                        str(row["session_id"]),
                        float(row["anomaly_score"]),
                        bool(row["is_anomalous"]),
                        MODEL_VERSION,
                        FEATURE_SET_VERSION,
                    ),
                )
        conn.commit()


def main() -> None:
    df = load_feature_data()
    print(f"[INFO] loaded {len(df)} session feature rows")

    if len(df) < 5:
        print("[WARN] very small dataset; anomaly results will be unstable")

    result_df = fit_and_score(df)
    persist_anomaly_results(result_df)

    sorted_df = result_df.sort_values(by="anomaly_score", ascending=True)

    print("[INFO] anomaly detection results:")
    for _, row in sorted_df.iterrows():
        print(
            f"[OK] session_id={row['session_id']} "
            f"score={row['anomaly_score']:.6f} "
            f"is_anomalous={bool(row['is_anomalous'])}"
        )

    print("[OK] Isolation Forest v1 completed successfully.")


if __name__ == "__main__":
    main()