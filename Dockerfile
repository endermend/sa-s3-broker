FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.14-slim-bookworm

RUN groupadd --system --gid 10000 nonroot \
    && useradd --system --gid 10000 --uid 10000 nonroot

RUN mkdir -p /files && chown nonroot:nonroot /files

WORKDIR /app

COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
COPY --from=builder --chown=nonroot:nonroot /app/src /app/src

COPY --chown=nonroot:nonroot start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENV PYTHONPATH="/app/src" \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    UPLOAD_DIR="/files"

USER nonroot

CMD ["/app/start.sh"]