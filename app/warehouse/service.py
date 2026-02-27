from fastapi import Depends, HTTPException
from .models.createItemModel import CreateItem
from .models.updateItemModel import UpdateItem
from app.warehouse.repository import WarehouseRepository

class WarehouseService:
    def __init__(self, repository: WarehouseRepository = Depends(WarehouseRepository)):
        self.repository = repository   
        
    async def get_items(self):
        getItems = await self.repository.get_items()
        return getItems

    async def add_item(self, item: CreateItem):
        newItems = await self.repository.add_item(item)
        return newItems
        
    async def get_item(self, item_id: int):
        getItem = await self.repository.get_item(item_id)
        return getItem
        
    async def update_item(self, item_id: int, newData: UpdateItem):
        if newData == {}:
            raise HTTPException(status_code=400, detail=f"You not change anything")
        newDataDict: dict = newData.model_dump(exclude_unset=True)
        updateItem = await self.repository.update_item(item_id, newDataDict)
        return updateItem
        