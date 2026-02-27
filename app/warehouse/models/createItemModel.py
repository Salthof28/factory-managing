from pydantic import BaseModel

class CreateItem(BaseModel):
    name: str
    price: float
    stock: int
    description: str | None = None
    