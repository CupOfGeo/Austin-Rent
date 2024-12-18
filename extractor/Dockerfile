FROM python:3.12 as BUILD

WORKDIR /app
EXPOSE 8080
RUN apt-get update && apt-get install -y age

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry
RUN poetry install --no-root

COPY . /app

ENTRYPOINT ["poetry", "run", "python", "-m", "scraper"]
