from __future__ import annotations

from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Annotated, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, ValidationError, field_validator


SchemaVersion = Literal["event_schema_v1"]
ProtocolType = Literal["ssh", "http"]
EventType = Literal[
    "ssh.session_start",
    "ssh.auth_attempt",
    "ssh.auth_result",
    "ssh.command_input",
    "ssh.command_executed",
    "ssh.session_end",
    "ssh.connection_closed",
    "http.request",
    "http.response",
    "http.probe_detected",
    "http.request_complete",
]


class EventMetadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    sensor_id: Optional[str] = None
    sensor_type: Optional[str] = None
    transport: Optional[str] = None
    ingest_source: Optional[str] = None
    capture_mode: Optional[str] = None


class SSHSessionStartPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connection_state: Literal["opened"]
    client_banner: Optional[str] = None
    server_banner: Optional[str] = None


class SSHAuthAttemptPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: Annotated[str, Field(min_length=1)]
    password: str
    auth_method: Literal["password", "publickey", "keyboard-interactive", "unknown"]


class SSHAuthResultPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    success: bool
    reason: Optional[str] = None


class SSHCommandInputPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    raw_command: Annotated[str, Field(min_length=1)]


class SSHCommandExecutedPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    normalized_command: Annotated[str, Field(min_length=1)]
    raw_command: Optional[str] = None


class SSHSessionEndPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    duration_seconds: float = Field(ge=0)
    end_reason: Optional[str] = None


class SSHConnectionClosedPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: Annotated[str, Field(min_length=1)]
    had_authenticated_session: Optional[bool] = None


PayloadType = Union[
    SSHSessionStartPayload,
    SSHAuthAttemptPayload,
    SSHAuthResultPayload,
    SSHCommandInputPayload,
    SSHCommandExecutedPayload,
    SSHSessionEndPayload,
    SSHConnectionClosedPayload,
    dict,
]


class PrometheusEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: SchemaVersion
    event_id: UUID
    timestamp: datetime
    protocol: ProtocolType
    source_ip: IPvAnyAddress
    source_port: int = Field(ge=1, le=65535)
    destination_port: int = Field(ge=1, le=65535)
    session_id: UUID
    event_sequence: int = Field(ge=1)
    event_type: EventType
    payload: PayloadType
    metadata: EventMetadata

    @field_validator("payload", mode="before")
    @classmethod
    def validate_payload_by_event_type(cls, value, info):
        event_type = info.data.get("event_type")
        protocol = info.data.get("protocol")

        if event_type is None:
            raise ValueError("event_type must be present before payload validation")

        if event_type.startswith("ssh.") and protocol != "ssh":
            raise ValueError("protocol must be 'ssh' for ssh.* event types")

        if event_type.startswith("http.") and protocol != "http":
            raise ValueError("protocol must be 'http' for http.* event types")

        payload_model_map = {
            "ssh.session_start": SSHSessionStartPayload,
            "ssh.auth_attempt": SSHAuthAttemptPayload,
            "ssh.auth_result": SSHAuthResultPayload,
            "ssh.command_input": SSHCommandInputPayload,
            "ssh.command_executed": SSHCommandExecutedPayload,
            "ssh.session_end": SSHSessionEndPayload,
            "ssh.connection_closed": SSHConnectionClosedPayload,
        }

        model = payload_model_map.get(event_type)
        if model is None:
            if not isinstance(value, dict):
                raise ValueError("payload must be an object")
            return value

        return model.model_validate(value)

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp must include timezone information")
        return value