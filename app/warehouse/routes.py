from fastapi import APIRouter, Depends
from .models.createItemModel import CreateItem
from .models.updateItemModel import UpdateItem
from app.warehouse.service import WarehouseService

# if you want code like nestjs
# class WarehouseController:
#     def __init__(self):
#         self.router = APIRouter()
#         # self.wareHouseService: WarehouseService = Depends(WarehouseService)
#         self.router.add_api_route("/", self.get_items, methods=["GET"])
        
#     async def get_items(self, wareHouseService: WarehouseService = Depends(WarehouseService)):
#         items = await wareHouseService.get_items()
#         return items

warehouse_router = APIRouter()

@warehouse_router.get("/")
async def get_items(warehouseService: WarehouseService = Depends(WarehouseService)):
    data = await warehouseService.get_items()
    return data
    
@warehouse_router.post("/", status_code=201)
async def add_item(item: CreateItem, warehouseService: WarehouseService = Depends(WarehouseService)):
    newData = await warehouseService.add_item(item)
    return newData
               
@warehouse_router.get("/{item_id}")
async def get_item(item_id: int, warehouseService: WarehouseService = Depends(WarehouseService)):
    data = await warehouseService.get_item(item_id)
    return data
    
@warehouse_router.patch("/{item_id}")
async def update_item(item_id: int, updateData: UpdateItem, warehouseService: WarehouseService = Depends(WarehouseService)):
    updateData = await warehouseService.update_item(item_id, updateData)
    return updateData