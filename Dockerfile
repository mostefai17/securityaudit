# Start with the official, standard Python image
FROM python:3.12-slim-trixie

# Set up your working directory and copyting UV binaries
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.5.0 /uv /uvx /bin/



# Disable development dependencies
ENV UV_SYSTEM_PYTHON=1
ENV UV_NO_DEV=1

COPY pyproject.toml uv.lock ./
RUN uv sync --locked

COPY . .

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

#FROM ubuntu:latest
#LABEL authors="mmi"
#
#ENTRYPOINT ["top", "-b"]