from fastapi import APIRouter, Depends, Query, status
from typing import List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.vacation_schema import VacationCreate, VacationResponse
from app.database.session import get_session
from app.services.vacation_service import VacationService

# Инициализация роутера для отпуска
router = APIRouter(prefix="/vacations", tags=["Отпуска"])


@router.post("/", response_model=VacationResponse, status_code=status.HTTP_201_CREATED)
async def create_vacation(
    vacation_data: VacationCreate,
    session: AsyncSession = Depends(get_session),
) -> VacationResponse:
    """
    Добавление нового отпуска сотрудника.
    """
    service = VacationService(session)
    return await service.create_vacation(vacation_data)


@router.get("/{employee_id}/latest", response_model=List[VacationResponse])
async def get_latest_vacations(
    employee_id: int,
    session: AsyncSession = Depends(get_session),
) -> List[VacationResponse]:
    """
    Получение 3 последних отпусков сотрудника.
    """
    service = VacationService(session)
    return await service.get_latest_vacations(employee_id)


@router.get("/", response_model=List[VacationResponse])
async def get_vacations_by_period(
    from_date: date = Query(..., description="Дата начала периода"),
    to_date: date = Query(..., description="Дата окончания периода"),
    session: AsyncSession = Depends(get_session),
) -> List[VacationResponse]:
    """
    Получение всех отпусков за указанный период.
    """
    service = VacationService(session)
    return await service.get_vacations_by_period(from_date, to_date)


@router.delete("/{vacation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacation(
    vacation_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Удаление отпуска по его ID.
    """
    service = VacationService(session)
    await service.delete_vacation(vacation_id)
