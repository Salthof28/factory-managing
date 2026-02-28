from pydantic import BaseModel
from .enum import EnumRoleUser

class LoginUser(BaseModel):
    email: str
    password: str