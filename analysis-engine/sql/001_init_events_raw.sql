CREATE TABLE IF NOT EXISTS events_raw (
    id BIGSERIAL PRIMARY KEY,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_timestamp TIMESTAMPTZ NOT NULL,
    protocol TEXT NOT NULL,
    source_ip INET NOT NULL,
    source_port INTEGER NOT NULL,
    destination_port INTEGER NOT NULL,
    session_id UUID NOT NULL,
    event_sequence INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    event_json JSONB NOT NULL,
    processing_error TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_raw_received_at
    ON events_raw (received_at DESC);

CREATE INDEX IF NOT EXISTS idx_events_raw_event_timestamp
    ON events_raw (event_timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_events_raw_session_id
    ON events_raw (session_id);

CREATE INDEX IF NOT EXISTS idx_events_raw_event_type
    ON events_raw (event_type);

CREATE INDEX IF NOT EXISTS idx_events_raw_protocol
    ON events_raw (protocol);

CREATE INDEX IF NOT EXISTS idx_events_raw_source_ip
    ON events_raw (source_ip);