FROM python:3.12-slim

WORKDIR /app

# Устанавливаем зависимости системы (если понадобятся для PostgreSQL и т.п.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN mkdir -p /app/storage

ENV DATABASE_URL=sqlite:///./app.db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
