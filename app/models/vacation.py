from sqlalchemy import Date, Integer, Column
from app.database.base import Base


class Vacation(Base):
    """
    Таблица отпусков:
    - Хранит периоды отпусков по `employee_id`;
    - Позволяет отслеживать пересечения и выборку по дате.
    """

    __tablename__ = "vacations"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
