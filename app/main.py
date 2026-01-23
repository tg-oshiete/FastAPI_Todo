from typing import Optional, Dict
from fastapi import FastAPI, HTTPException, status, Query
from models import TaskCreate, TaskResponse, TaskUpdate
from datetime import datetime
from fastapi import Response

app = FastAPI(title="My First API", version="0.1")

tasks_db: Dict[int, dict] = {}
task_counter = 0


@app.get("/tasks", response_model=list[TaskResponse])
async def read_tasks(
        skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
        limit: int = Query(10, ge=1, le=100, description="Лимит записей")
):
    """Получить все задачи"""
    tasks = list(tasks_db.values())
    tasks.sort(key=lambda x: x["id"])
    return tasks[skip:skip + limit]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int):
    """
    Получить конкретную задачу по ID.
    - **task_id** - int
    response: int:dict
    """
    if task_id in tasks_db:
        return tasks_db[task_id]
    else:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")


@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """
    Создать новую задачу

    - **title**: Заголовок (required)
    - **description**: Описание (Optional)
    - **completed**: Статус (default: False)
    """
    global task_counter
    task_counter += 1
    task_data = {
        "id": task_counter,
        **task.dict(),
        "created_at": datetime.now()
    }
    tasks_db[task_counter] = task_data
    return task_data


@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskCreate):
    """
    Обновление задачи.
    - **task**: TaskCreate
    - **task_id**: task_id
    """
    if task_id in tasks_db:
        current_task = tasks_db[task_id]
        updated_task = {
            "id": current_task["id"],  # System Field
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": current_task["created_at"],  # System field
            "updated_at": datetime.now()
        }
        tasks_db[task_id] = updated_task
        return updated_task
    else:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    if task_id in tasks_db:
        del tasks_db[task_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
async def patch_task(task_id: int, task: TaskUpdate):
    """
    Частично обновить задачу
    :param task_id: int
    :param task: TaskUpdate
    :return: TaskResponse
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail=f"Задача {task_id} не найдена")

    current_task = tasks_db[task_id]
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            current_task[key] = value
    current_task["updated_at"] = datetime.now()
    return current_task
