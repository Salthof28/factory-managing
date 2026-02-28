from fastapi import APIRouter, Depends
from .service import UserService
from .models.createUser import CreateUser

users_router = APIRouter()

@users_router.post("/", status_code=201)
async def signUp(dataUser: CreateUser, userService: UserService = Depends(UserService)):
    register = await userService.register(dataUser)
    return register