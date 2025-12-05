# Document Storage Service

Мини-сервис для хранения документов с версияцией, метаданными и базовым AI-анализом.

## Стек

- Python
- FastAPI
- SQLAlchemy (ORM)
- SQLite (по умолчанию, легко сменить на PostgreSQL через `DATABASE_URL`)
- Docker (опционально)

## Установка и запуск локально

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
