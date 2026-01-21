from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Модель для создания задачи"""
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskResponse(TaskCreate):
    """Модель для ответа с задачей"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True