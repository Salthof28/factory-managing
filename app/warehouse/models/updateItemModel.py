from pydantic import BaseModel

class UpdateItem(BaseModel):
    name: str | None = None
    price: float | None = None
    stock: int | None = None
    description: str | None = None