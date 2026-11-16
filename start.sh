#!/usr/bin/env bash
set -e

arq sa_s3_broker.infrastructure.arq_worker.WorkerSettings &
ARQ_PID=$!

gunicorn -c python:sa_s3_broker.gunicorn_conf \
        "sa_s3_broker.presentation.api.app_factory:create_app()" \
    & GUNICORN_PID=$!

shutdown() {
    echo "Received shutdown signal, stopping..."
    kill -TERM "$ARQ_PID" "$GUNICORN_PID" 2>/dev/null || true
    wait "$ARQ_PID" "$GUNICORN_PID" 2>/dev/null || true
    exit 0
}

trap shutdown TERM INT

wait -n "$ARQ_PID" "$GUNICORN_PID"

kill -TERM "$ARQ_PID" "$GUNICORN_PID" 2>/dev/null || true
wait "$ARQ_PID" "$GUNICORN_PID" 2>/dev/null || true