from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from fastapi import FastAPI, HTTPException, status, Query
# from in_memory_storage import tasks_db
from models import TaskCreate
from datetime import datetime



app = FastAPI(title="My First API", version="0.1")

# products = ["Стол", "Стул", "Мышка", "Печатная машинка", "Антон"]
tasks_db: Dict[int, dict] = {}
task_counter = 0


@app.get("/")
async def root():
    """
    Корневой эндпоинт.
    Возвращает приветственное сообщение.
    """
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Эндпоинт для получения элемента по ID.
    - **item_id**: Уникальный идентификатор элемента (целое число)
    """
    return {"item_id": item_id+100}

# @app.get("/products/{product_id}")
# async def read_item(product_id: int):
#     return {"product_id": product_id, "product": products[product_id]}


@app.get("/users/{username}")
async def read_user(username: str, active: bool = Query(True, description="Фильтр по активности пользователя")):
    return {"username":username, "active":active}


@app.get("/tasks")
async def read_tasks(): # формат вывода: {task_id}:int - task: dict
    """Получить все задачи"""
    print(tasks_db)
    data = dict()
    for idx, task in tasks_db.items():
        data[idx] = {"title": task["title"], "description": task["description"], "completed": task["completed"]}
    return data


@app.get("/tasks/{task_id}")
async def read_task(task_id:int):
    """
    Получить конкретную задачу по ID.
    - **task_id** - int
    response: int:dict
    """
    if task_id in tasks_db:
        return {task_id: {"title": tasks_db[task_id]["title"], "description": tasks_db[task_id]["description"],
                      "completed": tasks_db[task_id]["completed"]}}
    return "Not Found"


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
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


@app.put("/tasks/{task_id}")
async def update_task():
    pass


@app.delete("/tasks/{task_id}")
async def delete_task():
    pass
