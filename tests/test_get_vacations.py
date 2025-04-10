import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from app.main import app
from app.services.vacation_service import VacationService
from app.schemas.vacation_schema import VacationResponse
from typing import List


@pytest.mark.asyncio
async def test_get_vacations_success(monkeypatch) -> None:
    """
    Тест проверяет успешное получение отпусков по employee_id.
    Ожидается: HTTP 200 и список отпусков.
    """

    async def mock_get_vacations(self, employee_id: int) -> List[VacationResponse]:
        return [
            VacationResponse(
                id=1,
                employee_id=employee_id,
                start_date="2025-05-01",
                end_date="2025-05-10",
            )
        ]

    monkeypatch.setattr(VacationService, "get_latest_vacations", mock_get_vacations)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/vacations/1/latest")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert response.json()[0]["employee_id"] == 1


@pytest.mark.asyncio
async def test_get_vacations_invalid_employee(monkeypatch) -> None:
    """
    Тест проверяет поведение при отсутствии отпусков для employee_id.
    Ожидается: HTTP 200 и пустой список.
    """

    async def mock_get_vacations(self, employee_id: int) -> List[VacationResponse]:
        return []

    monkeypatch.setattr(VacationService, "get_latest_vacations", mock_get_vacations)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/vacations/9999/latest")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
