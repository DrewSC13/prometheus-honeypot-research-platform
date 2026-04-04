CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY,
    protocol TEXT NOT NULL,
    source_ip INET NOT NULL,
    source_port INTEGER NOT NULL,
    destination_port INTEGER NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    duration_seconds DOUBLE PRECISION NOT NULL,
    total_events INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sessions_start_time
    ON sessions (start_time DESC);

CREATE INDEX IF NOT EXISTS idx_sessions_source_ip
    ON sessions (source_ip);

CREATE INDEX IF NOT EXISTS idx_sessions_protocol
    ON sessions (protocol);


CREATE TABLE IF NOT EXISTS session_features (
    session_id UUID PRIMARY KEY REFERENCES sessions(session_id) ON DELETE CASCADE,
    num_attempts INTEGER NOT NULL,
    session_duration DOUBLE PRECISION NOT NULL,
    auth_failure_ratio DOUBLE PRECISION NOT NULL,
    unique_users INTEGER NOT NULL,
    unique_commands INTEGER NOT NULL,
    transition_auth_to_command_ratio DOUBLE PRECISION NOT NULL,
    cmd_token_entropy DOUBLE PRECISION NOT NULL,
    suspicious_token_ratio DOUBLE PRECISION NOT NULL,
    mean_dt DOUBLE PRECISION NOT NULL,
    std_dt DOUBLE PRECISION NOT NULL,
    burst_rate DOUBLE PRECISION NOT NULL,
    temporal_entropy DOUBLE PRECISION NOT NULL,
    feature_version TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_session_features_feature_version
    ON session_features (feature_version);