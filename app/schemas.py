from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Model for create task"""
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskResponse(TaskCreate):
    """Model for response task"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """Model for PATCH"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None