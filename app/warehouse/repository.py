from fastapi import Depends, HTTPException
from psycopg import AsyncConnection, sql
from .models.createItemModel import CreateItem
from app.warehouse import db_warehouse


class WarehouseRepository:
    def __init__(self, db: AsyncConnection = Depends(db_warehouse.con_db)):
        self.db = db
        
    async def get_items(self):
        async with self.db.cursor() as cur:
            await cur.execute("SELECT * FROM Warehouse")
            data = await cur.fetchall()
            # this is manual without dict_row
            # items = [{"id": datum[0], "name": datum[1], "price": datum[2], "stock": datum[3], "description": datum[4]} for datum in data]
            return data
        
    async def add_item(self, item: CreateItem):
        async with self.db.cursor() as cur:
            await cur.execute("INSERT INTO Warehouse (name, price, stock, description) VALUES(%s, %s, %s, %s) RETURNING *", (item.name, item.price, item.stock, item.description))
            data = await cur.fetchone()
            await self.db.commit()
            return data

    async def get_item(self, item_id: int):
        async with self.db.cursor() as cur:
            # if parameter only one use []. If you want use (), and paramater only one, add commas after parameter exp: (item_id,)
            await cur.execute("SELECT * FROM Warehouse WHERE id = %s", [item_id])
            data = await cur.fetchone()
            if not data:
                raise HTTPException(status_code=404, detail=f"item with id {item_id} not found")
            return data
        
    async def update_item(self, item_id: int, newDataDict: dict):
        fields: list[str] = []
        params: list = []
        for key, value in newDataDict.items():
            # use it if you not use sql composition
            # fields.append(f"{key} = %s")
            # use it if you use sql composition
            fields.append(sql.SQL("{field} = %s").format(field = sql.Identifier(key)))
            fields.append
            params.append(value)
        # create query without sql composition 
        # query = "UPDATE Warehouse SET " + ", ".join(fields) + " WHERE id = %s RETURNING *" 
        # create query with sql composition 
        query = sql.SQL("UPDATE {table} Set {field} WHERE {key} = %s RETURNING *").format(
            table = sql.Identifier('warehouse'),
            field = sql.SQL(', ').join(fields),
            key = sql.Identifier('id')
        )
        valueUpdate = tuple(params) + (item_id,)
        async with self.db.cursor() as cur:
            await cur.execute(query, valueUpdate)
            data = await cur.fetchone()
            await self.db.commit() 
            return data