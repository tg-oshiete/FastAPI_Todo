from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base


class TaskDB(Base):
    """Модель базы данных для задач"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    tittle = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
