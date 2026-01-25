from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List
from models import TaskDB
from schemas import TaskCreate, TaskUpdate

class TaskCRUD:
    @staticmethod
    async def create(db: AsyncSession, task: TaskCreate) -> TaskDB:
        """Create Task"""
        db_task = TaskDB(**task.dict())
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    @staticmethod
    async def get(db: AsyncSession, task_id: int) -> Optional[TaskDB]:
        """Get task by ID"""
        result = await db.execute(
            select(TaskDB).where(TaskDB.id == task_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) ->List[TaskDB]:
        """Get all tasks"""
        result = await db.execute(select(TaskDB).order_by(TaskDB.id).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update(db: AsyncSession, task_id:int, task_update: TaskUpdate) -> Optional[TaskDB]:
        """Update task"""
        update_data = task_update.dict(exclude_unset=True)

        if not update_data:
            return None

        await db.execute(update(TaskDB.where(TaskDB.id == task_id).values(**update_data)))
        await db.commit()
        return await TaskCRUD.get(db, task_id)


    @staticmethod
    async def delete(db: AsyncSession, task_id: int) -> bool:
        """Delete task"""
        task = await TaskCRUD.get(db, task_id)
        if task:
            await db.delete(task)
            await db.commit()
            return True
        return False