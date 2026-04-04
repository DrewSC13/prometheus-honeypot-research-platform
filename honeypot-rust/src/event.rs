use chrono::{SecondsFormat, Utc};
use serde::Serialize;
use serde_json::Value;
use uuid::Uuid;

#[derive(Debug, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub struct PrometheusEvent {
    pub schema_version: String,
    pub event_id: Uuid,
    pub timestamp: String,
    pub protocol: String,
    pub source_ip: String,
    pub source_port: u16,
    pub destination_port: u16,
    pub session_id: Uuid,
    pub event_sequence: u64,
    pub event_type: String,
    pub payload: Value,
    pub metadata: EventMetadata,
}

#[derive(Debug, Clone, Serialize)]
pub struct EventMetadata {
    pub sensor_id: String,
    pub sensor_type: String,
    pub transport: String,
    pub ingest_source: String,
    pub capture_mode: String,
}

impl EventMetadata {
    pub fn new(sensor_id: &str, ingest_source: &str) -> Self {
        Self {
            sensor_id: sensor_id.to_string(),
            sensor_type: "honeypot-rust".to_string(),
            transport: "stdout".to_string(),
            ingest_source: ingest_source.to_string(),
            capture_mode: "live".to_string(),
        }
    }
}

#[allow(clippy::too_many_arguments)]
impl PrometheusEvent {
    pub fn new(
        source_ip: String,
        source_port: u16,
        destination_port: u16,
        session_id: Uuid,
        event_sequence: u64,
        event_type: &str,
        payload: Value,
        metadata: EventMetadata,
    ) -> Self {
        Self {
            schema_version: "event_schema_v1".to_string(),
            event_id: Uuid::new_v4(),
            timestamp: Utc::now().to_rfc3339_opts(SecondsFormat::Secs, true),
            protocol: "ssh".to_string(),
            source_ip,
            source_port,
            destination_port,
            session_id,
            event_sequence,
            event_type: event_type.to_string(),
            payload,
            metadata,
        }
    }
}
