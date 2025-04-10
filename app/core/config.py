from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field
from functools import lru_cache


class Settings(BaseSettings):
    # Параметры PostgreSQL
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")

    @property
    def database_url(self) -> PostgresDsn:
        """
        Формирует строку подключения для PostgreSQL.
        """
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True  # Важно при использовании alias


@lru_cache()
def get_settings() -> Settings:
    """
    Возвращает объект настроек, загруженный из .env файла.
    """
    return Settings()
