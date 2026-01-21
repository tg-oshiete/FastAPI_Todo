from fastapi import FastAPI, Query



app = FastAPI(title="My First API", version="0.1")

# products = ["Стол", "Стул", "Мышка", "Печатная машинка", "Антон"]


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


# Создайте новый эндпоинт GET /users/{username}, который:
#
# Принимает username (строка) в пути.




@app.get("/users/{username}")
async def read_user(username: str, active: bool = Query(True, description="Фильтр по активности пользователя")):
    return {"username":username, "active":active}