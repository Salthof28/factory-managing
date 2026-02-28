from fastapi import APIRouter, Depends
from .service import UserService
from .models.createUser import CreateUser
from .models.login import LoginUser

users_router = APIRouter()

@users_router.post("/register", status_code=201)
async def signUp(dataUser: CreateUser, userService: UserService = Depends(UserService)):
    register = await userService.register(dataUser)
    return register

@users_router.post("/login")
async def login(dataLogin: LoginUser, userService: UserService = Depends(UserService)):
    signIn = await userService.login(dataLogin)
    return signIn