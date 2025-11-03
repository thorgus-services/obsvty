# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.7.1

WORKDIR /app

# Install minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}" \
    && poetry config virtualenvs.create false

# Copy dependency manifest and install
COPY pyproject.toml README.md ./
RUN poetry install --no-interaction --no-ansi --no-root

# Copy source and scripts
COPY src ./src
COPY tests ./tests
COPY generate_protos.py .
COPY .env.example .

# Generate proto stubs (allowed network call)
ARG OTLP_PROTO_REF=main
ENV OTLP_PROTO_REF=${OTLP_PROTO_REF}
RUN python generate_protos.py --ref ${OTLP_PROTO_REF}

# Default command
CMD ["bash"]