#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Starting Prometheus base services..."
docker compose up -d

echo "[INFO] Waiting for services to become healthy..."
sleep 5

docker compose ps

echo "[OK] Base services started."