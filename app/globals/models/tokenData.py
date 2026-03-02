from pydantic import BaseModel
from ...users.models.enum import EnumRoleUser
import datetime

class TokenData(BaseModel):
    id: int
    name: str
    role: EnumRoleUser
    exp: datetime.datetime
