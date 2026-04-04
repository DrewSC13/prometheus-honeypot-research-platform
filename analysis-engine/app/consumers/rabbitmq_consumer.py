from __future__ import annotations

import json
import os
from typing import Any

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pydantic import ValidationError

from app.db.postgres import get_connection, init_db, insert_invalid_raw_event, insert_raw_event
from app.models.event_models import PrometheusEvent


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "prom_bus")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "Popete13")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "prometheus.events.queue")


db_conn = None


def on_message(channel: BlockingChannel, method: Any, properties: Any, body: bytes) -> None:
    global db_conn

    raw_message = body.decode("utf-8", errors="replace")

    try:
        payload = json.loads(raw_message)
    except json.JSONDecodeError as exc:
        print("[INVALID_JSON]", exc)
        print(raw_message)
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    try:
        event = PrometheusEvent.model_validate(payload)
        insert_raw_event(db_conn, event)
        db_conn.commit()

        print(
            f"[OK] persisted event_type={event.event_type} "
            f"session_id={event.session_id} "
            f"source_ip={event.source_ip} "
            f"sequence={event.event_sequence}"
        )

        channel.basic_ack(delivery_tag=method.delivery_tag)

    except ValidationError as exc:
        error_text = str(exc)
        print("[INVALID_EVENT]")
        print(exc)
        insert_invalid_raw_event(db_conn, payload, error_text)
        db_conn.commit()
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as exc:
        db_conn.rollback()
        print("[DB_OR_PROCESSING_ERROR]", exc)
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main() -> None:
    global db_conn

    init_db()
    db_conn = get_connection()

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=10)

    print(
        "[INFO] RabbitMQ consumer with PostgreSQL persistence started "
        f"host={RABBITMQ_HOST} port={RABBITMQ_PORT} queue={RABBITMQ_QUEUE}"
    )

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=on_message,
        auto_ack=False,
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[INFO] Consumer interrupted by user.")
    finally:
        try:
            if not connection.is_closed:
                connection.close()
        finally:
            if db_conn is not None and not db_conn.closed:
                db_conn.close()


if __name__ == "__main__":
    main()