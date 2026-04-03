#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Stopping Prometheus base services..."
docker compose down

echo "[OK] Base services stopped."