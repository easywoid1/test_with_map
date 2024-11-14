FROM python:3.11-slim

WORKDIR /fastapi_app

COPY pyproject.toml poetry.lock /fastapi_app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY fastapi_app /fastapi_app

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
