FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as base
WORKDIR /app
ENV PATH="app/.venv/bin:$PATH"
EXPOSE 3000
ENTRYPOINT []

FROM base as dev
COPY ./pyproject.toml /app/pyproject.toml
RUN uv sync
CMD ["uv", "run", "app.py", "--debug"]

FROM base as prod
COPY . /app
RUN uv sync
CMD ["uv", "run", "app.py"]
