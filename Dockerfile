# ---------- Builder: install deps ----------
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libpq-dev \
    python3-dev

COPY pyproject.toml uv.lock README.md LICENSE ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv add gunicorn && \
    uv add whitenoise && \
    uv sync --frozen --no-editable --no-default-groups

COPY src/ ./src/

RUN . .venv/bin/activate && python -m compileall -q src

# ---------- Final: runtime ----------
FROM python:3.13-alpine

RUN apk add --no-cache \
    libpq \
    postgresql-client \
    curl \
    bash

RUN addgroup -S app && adduser -S -G app app
USER app

WORKDIR /app/src/aichhoernchen

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app src/ /app/src/
COPY --chown=app:app docker/start.sh /app/start.sh

RUN chmod +x /app/start.sh

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src/aichhoernchen/" \
    DJANGO_SETTINGS_MODULE=aichhoernchen.settings \
    PORT=8000

EXPOSE 8000

CMD ["/app/start.sh"]
