from fastapi import APIRouter, Depends
from typing import Annotated
from .service import UserService
from .models.createUser import CreateUser
from .models.login import LoginUser
from ..globals.guards import AuthGuard
from ..globals.models import TokenData
from fastapi.security import OAuth2PasswordBearer
from dotenv import dotenv_values

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
async def getProfile(auth: TokenData = Depends(AuthGuard()), userService: UserService = Depends(UserService)):
    myProfile = await userService.getProfile(auth)
    return myProfile