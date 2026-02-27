from pydantic import BaseModel
from .enum import EnumRoleUser

class CreateUser(BaseModel):
    name: str
    email: str
    phone: str | None = None
    password: str
    role: EnumRoleUser
    img_profile: str | None = None