from pydantic import BaseModel
from .enum import EnumRoleUser
import datetime

class TokenData(BaseModel):
    id: int
    name: str
    role: EnumRoleUser
    exp: datetime.datetime
