from fastapi import Depends, HTTPException, status
from typing import Annotated
from .repository import UsersRepository
from .models.createUser import CreateUser
from .models.login import LoginUser
from .models.responseUser import ResponseUser
from .models.tokenData import TokenData
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from dotenv import dotenv_values
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt


class UserService:
    def __init__(self, repository: UsersRepository = Depends(UsersRepository)):
        self.repository = repository
        self.configEnv = dotenv_values(".env")
        self.hashing_function = PasswordHash.recommended()
        
    async def register(self, newUser: CreateUser):
        # check email and phone existing in database
        findExisting = await self.repository.findExistingUser(newUser)
        if findExisting:
            if findExisting == "email":
                raise HTTPException(status_code=409, detail="this email registered")
            if findExisting == "phone":
                raise HTTPException(status_code=409, detail="this phone registered")
        # hashingb password
        password_concat = newUser.password + self.configEnv["SECRET_KEY_PASS"]
        password_hash = self.hashing_function.hash(password_concat)
        newUser.password = password_hash
        
        
        userNew = await self.repository.register(newUser)
        return userNew
    
    async def login(self, dataLogin: LoginUser):
        # get data user by email
        findUser: ResponseUser = await self.repository.findByEmail(dataLogin.email)
        if not findUser:
            HTTPException(status_code=404, detail=f"user with email {dataLogin.email} not found")
        # check password 
        password_concat = dataLogin.password + self.configEnv["SECRET_KEY_PASS"]
        password_check = self.hashing_function.verify(password_concat, findUser["password"])
        if not password_check:
            raise HTTPException(status_code=400, detail="password incorrect")
        expireToken = datetime.now(timezone.utc) + timedelta(minutes=15)
        encoded = jwt.encode({"id": findUser["id"], "name": findUser["name"], "role": findUser["role"], "exp": expireToken}, self.configEnv["key_JWT"], algorithm="HS256")
        # decoded = jwt.decode(encoded, self.configEnv["key_JWT"], algorithms="HS256")
        return encoded
    
    async def getProfile(self, token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validated credentials", headers={"WWW-Authenticate": "Bearer"})
        try:
            payload: TokenData = TokenData(**jwt.decode(token, self.configEnv["key_JWT"], algorithms="HS256"))
            getDataUser: ResponseUser = await self.repository.findById(payload.id)    
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expire")
        except InvalidTokenError:
            raise credentials_exception
        return getDataUser