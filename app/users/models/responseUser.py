from pydantic import BaseModel
from .enum import EnumRoleUser

class ResponseUser(BaseModel):
    name: str
    email: str
    phone: str | None
    password: str
    role: EnumRoleUser
    img_profile: str | None