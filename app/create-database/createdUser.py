from psycopg import AsyncConnection
from psycopg.rows import dict_row
from dotenv import dotenv_values
import asyncio
import selectors

config = dotenv_values(".env")

async def CreatedUSer():
    async with await AsyncConnection.connect(f"dbname={config["DB_NAME"]} user={config["USER"]} password={config["PASSWORD"]} host={config["HOST"]}", row_factory=dict_row) as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TYPE roles AS ENUM ('ADMIN', 'SUPERVISOR', 'STAFF')
                """)
            
            await cur.execute("""
                CREATE TABLE Users (
                    id serial PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(320) NOT NULL,
                    phone VARCHAR(20) NULL,
                    password VARCHAR(255) NOT NULL,
                    role roles,
                    img_profile TEXT NULL)  
                """)
        await conn.commit()
        
        
        
# if __name__ == "__main__":
# Create the compatible loop factory
loop_factory = lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())

# Run using the factory
asyncio.run(CreatedUSer(), loop_factory=loop_factory)