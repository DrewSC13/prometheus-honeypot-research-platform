CREATE TABLE IF NOT EXISTS anomalies (
    session_id UUID PRIMARY KEY REFERENCES sessions(session_id) ON DELETE CASCADE,
    anomaly_score DOUBLE PRECISION NOT NULL,
    is_anomalous BOOLEAN NOT NULL,
    model_version TEXT NOT NULL,
    feature_set_version TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_anomalies_model_version
    ON anomalies (model_version);

CREATE INDEX IF NOT EXISTS idx_anomalies_is_anomalous
    ON anomalies (is_anomalous);