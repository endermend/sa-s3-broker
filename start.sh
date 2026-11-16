#!/usr/bin/env bash
set -e

arq sa_s3_broker.infrastructure.arq_worker.WorkerSettings &
ARQ_PID=$!

gunicorn -c gunicorn_conf.py \
        "sa_s3_broker.presentation.api.app_factory:create_app()" \
    & GUVICORN_PID=$!

shutdown() {
    echo "Received shutdown signal, stopping..."
    kill -TERM "$ARQ_PID" "$GUVICORN_PID" 2>/dev/null || true
    wait "$ARQ_PID" "$GUVICORN_PID" 2>/dev/null || true
    exit 0
}

trap shutdown TERM INT

wait -n "$ARQ_PID" "$GUVICORN_PID"

kill -TERM "$ARQ_PID" "$GUVICORN_PID" 2>/dev/null || true
wait "$ARQ_PID" "$GUVICORN_PID" 2>/dev/null || true