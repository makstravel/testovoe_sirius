import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from app.main import app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Указание на использование asyncio в тестах.
    """
    return "asyncio"


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Фикстура для асинхронного клиента HTTP.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def mock_create_vacation(monkeypatch) -> None:
    """
    Мок для метода create_vacation() в VacationService.
    Используется в тестах создания отпуска.
    """
    from app.services import vacation_service

    async def mock_create(self, data):
        return {"id": 1, **data.model_dump()}

    monkeypatch.setattr(
        vacation_service.VacationService, "create_vacation", mock_create
    )


@pytest.fixture
def mock_delete_vacation(monkeypatch) -> None:
    """
    Мок для метода delete_vacation() в VacationService.
    Используется в тестах удаления отпуска.
    """
    from app.services import vacation_service

    async def mock_delete(self, vacation_id):
        return {"status": "deleted"}

    monkeypatch.setattr(
        vacation_service.VacationService, "delete_vacation", mock_delete
    )


@pytest.fixture
def mock_get_vacations(monkeypatch) -> None:
    """
    Мок для метода get_vacations_by_employee() в VacationService.
    Используется в тестах получения отпусков.
    """
    from app.services import vacation_service

    async def mock_get(self, employee_id):
        if employee_id == 999:
            return []
        return [
            {
                "id": 1,
                "employee_id": employee_id,
                "start_date": "2025-04-10",
                "end_date": "2025-04-15",
            }
        ]

    monkeypatch.setattr(
        vacation_service.VacationService, "get_latest_vacations", mock_get
    )
