from fastapi import Depends, HTTPException, status
from typing import Annotated
from ..models.tokenData import TokenData
from .auth import AuthGuard
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt

class RoleCheck:
    def __init__(self, roles: list[str]):
        self.allowed_roles = roles
        
        
    def __call__(self, user: TokenData = Depends(AuthGuard())):
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role not permitted")
        return user