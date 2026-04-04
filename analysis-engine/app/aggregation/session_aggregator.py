from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.db.postgres import get_connection


FEATURE_VERSION = "feature_set_v1"


@dataclass
class RawEvent:
    session_id: str
    protocol: str
    source_ip: str
    source_port: int
    destination_port: int
    event_timestamp: datetime
    event_sequence: int
    event_type: str
    event_json: dict[str, Any]


def fetch_ssh_raw_events() -> list[RawEvent]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    session_id,
                    protocol,
                    source_ip::text AS source_ip,
                    source_port,
                    destination_port,
                    event_timestamp,
                    event_sequence,
                    event_type,
                    event_json
                FROM events_raw
                WHERE protocol = 'ssh'
                ORDER BY session_id, event_sequence, event_timestamp
                """
            )
            rows = cur.fetchall()

    events: list[RawEvent] = []
    for row in rows:
        events.append(
            RawEvent(
                session_id=str(row["session_id"]),
                protocol=row["protocol"],
                source_ip=row["source_ip"],
                source_port=row["source_port"],
                destination_port=row["destination_port"],
                event_timestamp=row["event_timestamp"],
                event_sequence=row["event_sequence"],
                event_type=row["event_type"],
                event_json=row["event_json"],
            )
        )

    return events


def group_events_by_session(events: list[RawEvent]) -> dict[str, list[RawEvent]]:
    grouped: dict[str, list[RawEvent]] = defaultdict(list)
    for event in events:
        grouped[event.session_id].append(event)

    for session_id in grouped:
        grouped[session_id].sort(
            key=lambda e: (e.event_sequence, e.event_timestamp)
        )

    return grouped


def compute_session_summary(session_events: list[RawEvent]) -> dict[str, Any]:
    first = session_events[0]
    last = session_events[-1]

    start_time = first.event_timestamp
    end_time = last.event_timestamp
    duration_seconds = (end_time - start_time).total_seconds()

    total_events = len(session_events)

    usernames: set[str] = set()
    num_attempts = 0
    auth_results = 0
    auth_failures = 0

    for event in session_events:
        payload = event.event_json.get("payload", {})

        if event.event_type == "ssh.auth_attempt":
            num_attempts += 1
            username = payload.get("username")
            if username:
                usernames.add(username)

        if event.event_type == "ssh.auth_result":
            auth_results += 1
            if payload.get("success") is False:
                auth_failures += 1

    auth_failure_ratio = (
        auth_failures / auth_results if auth_results > 0 else 0.0
    )

    return {
        "session_id": first.session_id,
        "protocol": first.protocol,
        "source_ip": first.source_ip,
        "source_port": first.source_port,
        "destination_port": first.destination_port,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": duration_seconds,
        "total_events": total_events,
        "num_attempts": num_attempts,
        "unique_users": len(usernames),
        "auth_failure_ratio": auth_failure_ratio,
    }


def upsert_session_and_features(summary: dict[str, Any]) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sessions (
                    session_id,
                    protocol,
                    source_ip,
                    source_port,
                    destination_port,
                    start_time,
                    end_time,
                    duration_seconds,
                    total_events
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE SET
                    protocol = EXCLUDED.protocol,
                    source_ip = EXCLUDED.source_ip,
                    source_port = EXCLUDED.source_port,
                    destination_port = EXCLUDED.destination_port,
                    start_time = EXCLUDED.start_time,
                    end_time = EXCLUDED.end_time,
                    duration_seconds = EXCLUDED.duration_seconds,
                    total_events = EXCLUDED.total_events
                """,
                (
                    summary["session_id"],
                    summary["protocol"],
                    summary["source_ip"],
                    summary["source_port"],
                    summary["destination_port"],
                    summary["start_time"],
                    summary["end_time"],
                    summary["duration_seconds"],
                    summary["total_events"],
                ),
            )

            cur.execute(
                """
                INSERT INTO session_features (
                    session_id,
                    num_attempts,
                    session_duration,
                    auth_failure_ratio,
                    unique_users,
                    unique_commands,
                    transition_auth_to_command_ratio,
                    cmd_token_entropy,
                    suspicious_token_ratio,
                    mean_dt,
                    std_dt,
                    burst_rate,
                    temporal_entropy,
                    feature_version
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE SET
                    num_attempts = EXCLUDED.num_attempts,
                    session_duration = EXCLUDED.session_duration,
                    auth_failure_ratio = EXCLUDED.auth_failure_ratio,
                    unique_users = EXCLUDED.unique_users,
                    unique_commands = EXCLUDED.unique_commands,
                    transition_auth_to_command_ratio = EXCLUDED.transition_auth_to_command_ratio,
                    cmd_token_entropy = EXCLUDED.cmd_token_entropy,
                    suspicious_token_ratio = EXCLUDED.suspicious_token_ratio,
                    mean_dt = EXCLUDED.mean_dt,
                    std_dt = EXCLUDED.std_dt,
                    burst_rate = EXCLUDED.burst_rate,
                    temporal_entropy = EXCLUDED.temporal_entropy,
                    feature_version = EXCLUDED.feature_version
                """,
                (
                    summary["session_id"],
                    summary["num_attempts"],
                    summary["duration_seconds"],
                    summary["auth_failure_ratio"],
                    summary["unique_users"],
                    0,      # unique_commands
                    0.0,    # transition_auth_to_command_ratio
                    0.0,    # cmd_token_entropy
                    0.0,    # suspicious_token_ratio
                    0.0,    # mean_dt
                    0.0,    # std_dt
                    0.0,    # burst_rate
                    0.0,    # temporal_entropy
                    FEATURE_VERSION,
                ),
            )

        conn.commit()


def main() -> None:
    events = fetch_ssh_raw_events()
    grouped = group_events_by_session(events)

    print(f"[INFO] fetched {len(events)} SSH raw events")
    print(f"[INFO] detected {len(grouped)} SSH sessions")

    for session_id, session_events in grouped.items():
        summary = compute_session_summary(session_events)
        upsert_session_and_features(summary)

        print(
            f"[OK] aggregated session_id={session_id} "
            f"events={summary['total_events']} "
            f"attempts={summary['num_attempts']} "
            f"unique_users={summary['unique_users']} "
            f"duration={summary['duration_seconds']:.3f}s"
        )

    print("[OK] SSH session aggregation completed.")


if __name__ == "__main__":
    main()