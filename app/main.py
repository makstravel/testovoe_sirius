"""
Главная точка входа в приложение FastAPI.
Инициализирует FastAPI-приложение и подключает маршруты.
"""

from fastapi import FastAPI
from app.api.routers.vacation_router import router as vacation_router

# Создание экземпляра FastAPI с заголовком
app = FastAPI(title="Сервис управления отпусками")

# Подключение маршрутов приложения (роутер отпусков)
app.include_router(vacation_router)
