FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install the project into `/app`
WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["fastapi", "dev", "--host", "0.0.0.0", "/app/app/main.py"]
