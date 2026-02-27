from fastapi import FastAPI
from app.warehouse.routes import warehouse_router
# from app.warehouse.routes import WarehouseController

app = FastAPI()
# warehouseController = WarehouseController()

app.include_router(warehouse_router, prefix="/warehouse", tags=["warehouse"])