#!/usr/bin/env bash
set -e

arq sa_s3_broker.infrastructure.arq_worker.WorkerSettings &
ARQ_PID=$!

uvicorn sa_s3_broker.presentation.api.app_factory:create_app \
    --factory \
    --host 0.0.0.0 \
    --port "${APP_PORT:-8000}" &
UVICORN_PID=$!

shutdown() {
    echo "Received shutdown signal, stopping..."
    kill -TERM "$ARQ_PID" "$UVICORN_PID" 2>/dev/null || true
    wait "$ARQ_PID" "$UVICORN_PID" 2>/dev/null || true
    exit 0
}

trap shutdown TERM INT

wait -n "$ARQ_PID" "$UVICORN_PID"

kill -TERM "$ARQ_PID" "$UVICORN_PID" 2>/dev/null || true
wait "$ARQ_PID" "$UVICORN_PID" 2>/dev/null || true