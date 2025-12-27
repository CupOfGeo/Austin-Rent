FROM python:3.12-slim

WORKDIR /app
EXPOSE 8080

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    age \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock /app/

# Install dependencies (without the project itself)
RUN uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . /app

# Sync again to install the project
RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "python", "-m", "scraper"]
