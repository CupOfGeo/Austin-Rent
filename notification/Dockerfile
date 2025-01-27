# syntax=docker/dockerfile:1.4

FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Create non-root user
RUN groupadd -r notifier && useradd -r -g notifier notifier

# Copy application code and requirements
COPY requirements.txt .
COPY notification/ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Switch to non-root user
USER notifier

# Command to run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app