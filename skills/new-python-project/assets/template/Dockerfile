# Stages:
#   builder  resolve dependencies from uv.lock, install the project as a wheel
#   dev      local development (dev tools, editable install); used by compose.yaml
#   runtime  production image (default target, last stage)

FROM ghcr.io/astral-sh/uv:0.13.7-python3.12-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Dependencies first, for layer caching.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

# Then the project itself. --no-editable copies it into the venv; /app source is not needed later.
COPY README.md ./
COPY src ./src
RUN uv sync --locked --no-dev --no-editable


FROM ghcr.io/astral-sh/uv:0.13.7-python3.12-trixie-slim AS dev

# The venv lives outside /app, so the bind mount of the repository does not hide it.
# UV_NO_SYNC: `uv run` does not change the venv at run time. Rebuild after a dependency change.
ENV UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_NO_SYNC=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    HOME=/tmp

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project
COPY README.md ./
COPY src ./src
RUN uv sync --locked && chmod -R a+rX /opt/venv

CMD ["my-project", "--help"]


FROM python:3.12-slim-trixie AS runtime

RUN useradd --create-home --shell /usr/sbin/nologin app \
    && mkdir -p /data/output && chown -R app:app /data
COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    MY_PROJECT_OUTPUT_DIR=/data/output

USER app
WORKDIR /data

ENTRYPOINT ["my-project"]
CMD ["--help"]
