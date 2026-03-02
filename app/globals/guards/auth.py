from fastapi import Depends, HTTPException, status
from typing import Annotated
from ..models.tokenData import TokenData
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt

class AuthGuard:
    def __init__(self):
        self.configEnv = dotenv_values(".env")
        
    def __call__(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validated credentials", headers={"WWW-Authenticate": "Bearer"})
        try:
            payload: TokenData = TokenData(**jwt.decode(token, self.configEnv["key_JWT"], algorithms="HS256"))
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expire")
        except InvalidTokenError:
            raise credentials_exception
        return payload