import pytest
from fastapi import status, HTTPException
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.vacation_service import VacationService


@pytest.mark.asyncio
async def test_create_vacation_success(monkeypatch) -> None:
    """
    Тест проверяет успешное создание отпуска.
    Ожидается: HTTP 201 и корректный `employee_id` в ответе.
    """

    async def mock_create_vacation(self: VacationService, vacation_data) -> dict:
        return {"id": 1, **vacation_data.model_dump()}

    monkeypatch.setattr(VacationService, "create_vacation", mock_create_vacation)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/vacations/",
            json={
                "employee_id": 1,
                "start_date": "2025-04-15",
                "end_date": "2025-04-20",
            },
        )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["employee_id"] == 1


@pytest.mark.asyncio
async def test_create_vacation_overlap(monkeypatch) -> None:
    """
    Тест проверяет случай перекрытия отпусков.
    Ожидается: HTTP 400 и сообщение об ошибке.
    """

    async def mock_create_vacation(self: VacationService, vacation_data) -> None:
        raise HTTPException(status_code=400, detail="Overlapping vacation")

    monkeypatch.setattr(VacationService, "create_vacation", mock_create_vacation)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/vacations/",
            json={
                "employee_id": 1,
                "start_date": "2025-04-15",
                "end_date": "2025-04-20",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Overlapping vacation"
