import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.pool import NullPool
from alembic import context
from app.core.config import get_settings
from app.database.base import Base
from app.models.vacation import Vacation

# Загружаем настройки из .env
settings = get_settings()

# Конфигурация Alembic
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем строку подключения к БД в Alembic конфиг
DATABASE_URL = settings.database_url
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Мета-данные модели для Alembic (автогенерация)
target_metadata = Base.metadata


def run_migrations_offline():
    """Оффлайн-режим — без подключения к БД"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Запуск миграций в подключённой сессии"""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Онлайн-режим — с подключением к asyncpg"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=NullPool,
        future=True,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
