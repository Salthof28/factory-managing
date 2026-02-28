from fastapi import FastAPI
from app.users import users_router
from app.warehouse.routes import warehouse_router
# from app.warehouse.routes import WarehouseController

app = FastAPI()
# warehouseController = WarehouseController()

app.include_router(warehouse_router, prefix="/warehouse", tags=["Warehouse"])
app.include_router(users_router, prefix="/users", tags=["Users"])