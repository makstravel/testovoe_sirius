from app.schemas.vacation_schema import VacationCreate
from app.repositories.vacation_repository import VacationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import date
from typing import List
from app.models.vacation import Vacation


class VacationService:
    """
    Сервисный слой для обработки логики управления отпусками сотрудников.
    """

    def __init__(self, session: AsyncSession):
        self.repo = VacationRepository(session)

    async def create_vacation(self, vacation_data: VacationCreate) -> Vacation:
        """
        Создание отпуска с проверкой пересечений по датам.
        """
        overlap = await self.repo.check_overlap(
            vacation_data.employee_id,
            vacation_data.start_date,
            vacation_data.end_date,
        )
        if overlap:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Даты отпуска пересекаются с уже существующим отпуском.",
            )
        return await self.repo.add_vacation(vacation_data)

    async def get_latest_vacations(self, employee_id: int) -> List[Vacation]:
        """
        Получить 3 последних отпуска сотрудника.
        """
        return await self.repo.get_last_three_by_employee(employee_id)

    async def get_vacations_by_period(
        self, from_date: date, to_date: date
    ) -> List[Vacation]:
        """
        Получить отпуска всех сотрудников за указанный период.
        """
        return await self.repo.get_by_period(from_date, to_date)

    async def delete_vacation(self, vacation_id: int) -> None:
        """
        Удалить отпуск по ID. Если отпуск не найден — вернуть 404.
        """
        vacation = await self.repo.get_by_id(vacation_id)
        if not vacation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Отпуск с ID {vacation_id} не найден.",
            )
        await self.repo.delete(vacation)
