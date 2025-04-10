from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

settings = get_settings()
# Создание асинхронного движка подключения к базе данных
engine = create_async_engine(str(settings.database_url), echo=True)

# Создание асинхронной сессии с БД
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)


# Базовый класс для всех моделей SQLAlchemy
class Base(DeclarativeBase):
    pass


# Асинхронный генератор сессий БД
async def get_db() -> AsyncSession:
    """
    Предоставляет асинхронную сессию базы данных
    для использования в маршрутах и сервисах.
    """
    async with SessionLocal() as session:
        yield session
