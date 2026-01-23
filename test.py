from pydantic import BaseModel
from typing import Optional

order = {
    "блюдо": "паста",
    "напиток": "кола",
    "количество": "два"
}


class Order(BaseModel):
    dish: str
    drink: Optional[str] = None
    amount: int = 1


order1 = Order(dish="Глазунья", amount=2)
print(type(order1))
print(order1)

_dict = {
    1: {2: "Hello", 3: "Goodbye"},
    2: {3: {"hello"}},
    3: "Hi"
}

# print(list(_dict.values()))
print(_dict[1:2])
