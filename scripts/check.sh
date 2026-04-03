#!/usr/bin/env bash
set -euo pipefail

if [[ -f ".env" ]]; then
  set -a
  source .env
  set +a
fi

echo "[INFO] Checking Docker Compose service status..."
docker compose ps

echo
echo "[INFO] Checking PostgreSQL health..."
POSTGRES_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' prometheus-postgres 2>/dev/null || echo "\"not-found\"")
echo "PostgreSQL health: ${POSTGRES_STATUS}"

echo
echo "[INFO] Checking RabbitMQ health..."
RABBITMQ_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' prometheus-rabbitmq 2>/dev/null || echo "\"not-found\"")
echo "RabbitMQ health: ${RABBITMQ_STATUS}"

echo
echo "[INFO] Connection summary:"
echo "PostgreSQL -> localhost:${POSTGRES_PORT:-5432}"
echo "RabbitMQ AMQP -> localhost:${RABBITMQ_AMQP_PORT:-5672}"
echo "RabbitMQ UI -> http://localhost:${RABBITMQ_MANAGEMENT_PORT:-15672}"

if [[ "${POSTGRES_STATUS}" == "\"healthy\"" && "${RABBITMQ_STATUS}" == "\"healthy\"" ]]; then
  echo
  echo "[OK] All base services are healthy."
else
  echo
  echo "[WARN] One or more services are not healthy yet."
fi