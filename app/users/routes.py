from fastapi import APIRouter, Depends
from typing import Annotated
from .service import UserService
from .models.createUser import CreateUser
from .models.login import LoginUser
from fastapi.security import OAuth2PasswordBearer

users_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@users_router.post("/register", status_code=201)
async def signUp(dataUser: CreateUser, userService: UserService = Depends(UserService)):
    register = await userService.register(dataUser)
    return register

@users_router.post("/login")
async def login(dataLogin: LoginUser, userService: UserService = Depends(UserService)):
    signIn = await userService.login(dataLogin)
    return signIn

@users_router.post("/profile")
async def getProfile(token: Annotated[str, Depends(oauth2_scheme)] ,userService: UserService = Depends(UserService)):
    myProfile = await userService.getProfile(token)
    return myProfile