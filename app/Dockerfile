FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base
WORKDIR /app
ENV PATH="app/.venv/bin:$PATH"
EXPOSE 3000
ENTRYPOINT []
COPY ./pyproject.toml /app/pyproject.toml
RUN uv sync

FROM base AS dev
CMD ["uv", "run", "app.py", "--debug"]

FROM base AS prod
COPY . /app
CMD ["uv", "run", "app.py"]
