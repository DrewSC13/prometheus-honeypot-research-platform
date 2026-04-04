from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.models.event_models import PrometheusEvent


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5433"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "prometheus_vault")
POSTGRES_USER = os.getenv("POSTGRES_USER", "prom_archiver")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Popete13")


def get_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        row_factory=dict_row,
    )


def init_db() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    sql_file = repo_root / "analysis-engine" / "sql" / "001_init_events_raw.sql"
    sql = sql_file.read_text(encoding="utf-8")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


def insert_raw_event(conn: psycopg.Connection, event: PrometheusEvent) -> None:
    event_dict = event.model_dump(mode="json")
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO events_raw (
                event_timestamp,
                protocol,
                source_ip,
                source_port,
                destination_port,
                session_id,
                event_sequence,
                event_type,
                event_json,
                processing_error
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s)
            """,
            (
                event.timestamp,
                event.protocol,
                str(event.source_ip),
                event.source_port,
                event.destination_port,
                str(event.session_id),
                event.event_sequence,
                event.event_type,
                json.dumps(event_dict),
                None,
            ),
        )


def insert_invalid_raw_event(conn: psycopg.Connection, payload: dict[str, Any], error_text: str) -> None:
    protocol = payload.get("protocol", "unknown")
    source_ip = payload.get("source_ip", "0.0.0.0")
    source_port = payload.get("source_port", 0)
    destination_port = payload.get("destination_port", 0)
    session_id = payload.get("session_id", "00000000-0000-0000-0000-000000000000")
    event_sequence = payload.get("event_sequence", 0)
    event_type = payload.get("event_type", "invalid.unknown")
    event_timestamp = payload.get("timestamp", "1970-01-01T00:00:00Z")

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO events_raw (
                event_timestamp,
                protocol,
                source_ip,
                source_port,
                destination_port,
                session_id,
                event_sequence,
                event_type,
                event_json,
                processing_error
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s)
            """,
            (
                event_timestamp,
                protocol,
                source_ip,
                source_port,
                destination_port,
                session_id,
                event_sequence,
                event_type,
                json.dumps(payload),
                error_text,
            ),
        )