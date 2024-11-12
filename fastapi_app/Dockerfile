FROM python:3.11-slim

WORKDIR /fastapi_app

COPY ../pyproject.toml poetry.lock /fastapi_app/

# Устанавливаем Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY fastapi_app /fastapi_app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--port", "8000"]


