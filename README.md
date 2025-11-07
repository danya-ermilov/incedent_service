# 🧭 Incidents API

Маленький API-сервис для учёта инцидентов (операторов, партнёров, систем мониторинга).  
Помогает не терять сообщения о проблемах вроде «самокат не в сети» или «отчёт не выгрузился».

---

## Возможности

- Создание инцидента  
- Получение списка инцидентов (с фильтрацией по статусу и источнику)  
- Обновление статуса инцидента  
- Полная OpenAPI-документация через Swagger UI

---

## Технологии

- [FastAPI](https://fastapi.tiangolo.com/) — фреймворк для REST API  
- [SQLAlchemy 2.0 (async)](https://docs.sqlalchemy.org/en/20/) — ORM  
- [PostgreSQL](https://www.postgresql.org/) — база данных  
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) — миграции  
- [Pydantic](https://docs.pydantic.dev/) — валидация схем  

---

## Структура проекта
```bash
app/
├── api/
│ └── routes.py # Эндпоинты API
├── core/
│ └── config.py # Настройки (ENV)
├── crud/
│ └── init.py # CRUD-логика (операции с БД)
├── db/
│ ├── session.py # Асинхронная сессия SQLAlchemy
│ └── base.py # Подключение Base моделей
├── models/
│ └── incident.py # Модель Incident
├── schemas/
│ └── incident.py # Pydantic-схемы
└── main.py # Точка входа FastAPI
migrations/
└── versions/ # Alembic-миграции
.env # Переменные окружения
requirements.txt # Зависимости
```

---

## Настройка окружения

1. Установи зависимости:

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

2. Создай PostgreSQL-базу:
```bash
sudo -u postgres psql
CREATE DATABASE incidents_db;
CREATE USER incidents_user WITH PASSWORD 'password';
ALTER ROLE incidents_user SET client_encoding TO 'utf8';
ALTER ROLE incidents_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE incidents_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE incidents_db TO incidents_user;
\q
```

3. Добавь файл .env в корень проекта:
```bash
DATABASE_URL=postgresql+asyncpg://incidents_user:password@localhost:5432/incidents_db
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
```

4. Примените миграции:
```bash
alembic upgrade head
```


## Запуск
```bash
uvicorn app.main:app --reload
```

После запуска открой:
Swagger UI: http://127.0.0.1:8000/docs


## Примеры запросов
Создать инцидент

POST /incidents
```json
{
  "description": "Самокат не в сети",
  "source": "operator"
}
```

Получить список инцидентов

GET /incidents

Возможные параметры:

status: new / in_progress / resolved / closed

Пример:

GET /incidents?status=in_progress

Обновить статус

PATCH /incidents/{incident_id}
```json

{
  "status": "resolved"
}
```
