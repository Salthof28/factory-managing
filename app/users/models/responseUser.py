from pydantic import BaseModel
from .enum import EnumRoleUser
import datetime

class ResponseUser(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    password: str
    role: EnumRoleUser
    img_profile: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime