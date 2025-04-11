# Сервис Управления Отпуском API

Тестовое заданиие - Сервис управления отпусками сотрудников.

## 🛠 Используемые технологии

- **FastAPI** — основной фреймворк
- **SQLAlchemy 2.0** — ORM
- **Alembic** — миграции
- **pytest** — тестирование
- **Pydantic** — валидация
- 
---

## 🚀 Запуск проекта 

Скачайте проект 

```bash
git clone https://github.com/makstravel/testovoe_sirius.git && cd testovoe_sirius
```


> Создайте базу данных vacation_db
```bash
psql -U postgres
```
```bash
CREATE DATABASE vacation_db;
```
> Убедитесь, что PostgreSQL запущен, и в системе создана база данных `vacation_db`.




1. Установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Создайте файл `.env` на основе следующего шаблона:

```env
POSTGRES_USER=...
POSTGRES_PASSWORD=..
POSTGRES_DB=..
POSTGRES_HOST=..
POSTGRES_PORT=..

```

3. Примените миграции:

```bash
alembic revision --autogenerate -m "Init migration"
```

```bash
alembic upgrade head
```

4. Запустите сервер:

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Запуск тестов

```bash
pytest
```

---

## 📘 Документация API

Swagger-документация доступна по адресу:  
```
http://localhost:8000/docs
```

### Примеры эндпоинтов:

#### 🔹 Создание отпуска
`POST /vacations/`

```json
{
  "employee_id": 1,
  "start_date": "2025-06-01",
  "end_date": "2025-06-10"
}
```

#### 🔹 Получение всех отпусков
`GET /vacations/`

#### 🔹 Получение отпусков за период
`GET /vacations/?start_date=2025-06-01&end_date=2025-06-30`

#### 🔹 Удаление отпуска
`DELETE /vacations/{vacation_id}`

---

## ✅ Pre-commit Hooks

Проект поддерживает проверку стиля и типов:

```bash
pre-commit install
pre-commit run --all-files
```

---






