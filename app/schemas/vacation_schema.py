from datetime import date
from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Optional


class VacationBase(BaseModel):
    """
    Базовая схема отпуска (используется при создании и выводе).
    """

    employee_id: int
    start_date: date
    end_date: date

    @field_validator("end_date")
    def validate_dates(cls, end_date: date, info: ValidationInfo) -> date:
        """
        Проверка, что дата окончания отпуска не раньше даты начала.
        """
        start_date: Optional[date] = info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("Дата окончания должна быть после даты начала")
        return end_date


class VacationCreate(VacationBase):
    """
    Схема запроса на создание отпуска.
    """

    pass


class VacationResponse(VacationBase):
    """
    Схема ответа с данными об отпуске, включая ID.
    """

    id: int

    class Config:
        from_attributes = True
