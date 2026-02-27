from psycopg import AsyncConnection
from psycopg.rows import dict_row
from dotenv import dotenv_values

# # load variabel in .env file
# config = dotenv_values(".env")

class Db_connect:
    def __init__(self):
        config = dotenv_values(".env")
        self.db_name = config["DB_NAME"]
        self.user = config["USER"]
        self.password = config["PASSWORD"]
        self.host = config["HOST"]
    
    async def con_db(self):
        async with await AsyncConnection.connect(f"dbname={self.db_name} user={self.user} password={self.password} host={self.host} port=5432", row_factory=dict_row) as conn:
            yield conn


db_connect = Db_connect()