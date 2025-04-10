import pytest
from fastapi import status, HTTPException
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.vacation_service import VacationService


@pytest.mark.asyncio
async def test_delete_vacation_success(monkeypatch) -> None:
    """
    Тест проверяет успешное удаление отпуска.
    Ожидается: HTTP 204 (No Content).
    """

    async def mock_delete_vacation(self: VacationService, vacation_id: int) -> None:
        return None  # Удаление успешно

    monkeypatch.setattr(VacationService, "delete_vacation", mock_delete_vacation)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.delete("/vacations/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_vacation_not_found(monkeypatch) -> None:
    """
    Тест проверяет поведение при удалении несуществующего отпуска.
    Ожидается: HTTP 404 и сообщение "Vacation not found".
    """

    async def mock_delete_vacation(self: VacationService, vacation_id: int) -> None:
        raise HTTPException(status_code=404, detail="Vacation not found")

    monkeypatch.setattr(VacationService, "delete_vacation", mock_delete_vacation)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.delete("/vacations/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Vacation not found"
