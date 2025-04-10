from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base  # Используйте правильный импорт
from app.core.config import get_settings
from dotenv import load_dotenv

load_dotenv()

settings = get_settings()

# URL для подключения к БД
DATABASE_URL = settings.database_url

# Инициализация асинхронного движка SQLAlchemy
engine = create_async_engine(
    DATABASE_URL, echo=True, future=True  # Вывод SQL-запросов в лог для отладки
)

# Создаём асинхронную фабрику сессий
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Используйте declarative_base вместо DeclarativeBase
Base = declarative_base()


# Зависимость FastAPI
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
