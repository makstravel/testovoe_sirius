from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.vacation import Vacation
from app.schemas.vacation_schema import VacationCreate
from datetime import date
from typing import List, Optional


class VacationRepository:
    """
    Репозиторий для управления данными об отпусках сотрудников.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_vacation(self, vacation_data: VacationCreate) -> Vacation:
        """
        Добавляет новый отпуск сотрудника.
        """
        vacation = Vacation(**vacation_data.model_dump())
        self.session.add(vacation)
        await self.session.commit()
        await self.session.refresh(vacation)
        return vacation

    async def get_last_three_by_employee(self, employee_id: int) -> List[Vacation]:
        """
        Возвращает 3 последних отпуска по дате начала для конкретного сотрудника.
        """
        result = await self.session.execute(
            select(Vacation)
            .where(Vacation.employee_id == employee_id)
            .order_by(desc(Vacation.start_date))
            .limit(3)
        )
        # Указываем, что результат будет списком объектов Vacation
        return result.scalars().all()

    async def get_by_period(self, from_date: date, to_date: date) -> List[Vacation]:
        """
        Возвращает все отпуска за указанный период.
        """
        result = await self.session.execute(
            select(Vacation).where(
                and_(
                    Vacation.start_date <= to_date,
                    Vacation.end_date >= from_date,
                )
            )
        )
        return result.scalars().all()

    async def get_by_id(self, vacation_id: int) -> Optional[Vacation]:
        """
        Получает отпуск по его ID.
        """
        result = await self.session.execute(
            select(Vacation).where(Vacation.id == vacation_id)
        )
        # Если нет отпуска, возвращаем None
        return result.scalar_one_or_none()

    async def delete(self, vacation: Vacation) -> None:
        """
        Удаляет указанный объект отпуска.
        """
        await self.session.delete(vacation)
        await self.session.commit()

    async def check_overlap(
        self, employee_id: int, start_date: date, end_date: date
    ) -> bool:
        """
        Проверяет наличие пересечений отпусков для сотрудника.
        """
        result = await self.session.execute(
            select(Vacation).where(
                and_(
                    Vacation.employee_id == employee_id,
                    Vacation.start_date <= end_date,
                    Vacation.end_date >= start_date,
                )
            )
        )
        # Если такой отпуск найден, возвращаем True
        return result.first() is not None
