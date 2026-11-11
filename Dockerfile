# Start with the official, standard Python image
FROM python:3.12-slim-bookworm AS builder

# Set up your working directory and copyting UV binaries
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.5.0 /uv /uvx /bin/
# Copy configuration files for dependancy installaiton
COPY pyproject.toml uv.lock ./

# Sync dependencies without dev packages into a dedicated virtualenv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Stage 2: Final minimal runtinme image

FROM python:3.12-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY . .

#Place the virual environment binaries directly into the PATH
ENV PATH="/app/.venv/bin:$PATH"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
