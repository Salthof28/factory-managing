from fastapi import Depends, HTTPException
from .repository import UsersRepository
from .models.createUser import CreateUser
from pwdlib import PasswordHash
from dotenv import dotenv_values

class UserService:
    def __init__(self, repository: UsersRepository = Depends(UsersRepository)):
        self.repository = repository
        self.configEnv = dotenv_values(".env")
        
    async def register(self, newUser: CreateUser):
        # check email and phone existing in database
        findExisting = await self.repository.findExistingUser(newUser)
        if findExisting:
            if findExisting == "email":
                raise HTTPException(status_code=409, detail="This email registered")
            if findExisting == "phone":
                raise HTTPException(status_code=409, detail="This phone registered")
        # hashingb password
        hashing_function = PasswordHash.recommended()
        password_concat = newUser.password + self.configEnv["SECRET_KEY_PASS"]
        password_hash = hashing_function.hash(password_concat)
        newUser.password = password_hash
        
        
        userNew = await self.repository.register(newUser)
        return userNew
    