FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install the project dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the container
COPY . /app

ENTRYPOINT ["poetry", "run", "python", "-m", "bs-crawler"]