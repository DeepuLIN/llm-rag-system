FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN useradd -m appuser

COPY requirements-docker.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements-docker.txt

COPY src ./src
COPY main.py .
COPY data/knowledge-base ./data/knowledge-base

RUN mkdir -p /app/vector_db && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.api.api:app", "--host", "0.0.0.0", "--port", "8000"]