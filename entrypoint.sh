#!/bin/bash
set -e

export PATH="/root/.local/bin:$PATH"

cd /app

echo "Applying database migrations..."
uv run alembic upgrade head

# Запускаем consumer в фоне
uv run python -m bin.consumer &

# Запускаем API (без exec, чтобы shell ждал)
uv run python -m bin.api
