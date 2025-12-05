# Document Storage Service

Мини-сервис для хранения документов с версияцией, метаданными и базовым AI-анализом.

## Стек

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Docker

## Установка и запуск локально

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
