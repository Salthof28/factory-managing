from psycopg import AsyncConnection
from pwdlib import PasswordHash
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
                    img_profile TEXT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP)  
                """)
            
            # create script logic automatic trigger in row update_at
            # CREATE OR REPLACE FUNCTION update_updated_at_column(), this is for create function and replace function, if the function is exist
            # RETURNS TRIGGER, this is for notify that this running, if have trigger
            # AS $$ ... $$, this is quition mark
            # BEGIN ... END; this marker start program and end program (container script)
            # NEW.updated_at = CURRENT_TIMESTAMP;. NEW is key represent new data version recently update
            # RETURN NEW; new data can save in tabel
            # language 'plpgsql'; information, this function write used postgres
            await cur.execute("""            
                CREATE OR REPLACE FUNCTION trigger_update_at()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ language 'plpgsql'
                """)
            
            # insert script in table Users
            # CREATE TRIGGER trigger_update_users. create trigger with name users_triger_update_at
            # BEFORE UPDATE ON users. run the script before data changed. Use this because for put in new time before data locked in database
            # FOR EACH ROW. Do this, each value in row table changed
            # EXECUTE PROCEDURE update_updated_at_column(). If the requirement fulfilled, run the script trigger_update_at()
            await cur.execute("""
                CREATE TRIGGER users_triger_update_at
                BEFORE UPDATE ON Users
                FOR EACH ROW 
                EXECUTE PROCEDURE trigger_update_at();
                """)
            # admin user
            password_hash = PasswordHash.recommended()
            password = "admin123"
            password_concat = password + config["SECRET_KEY_PASS"]
            hash = password_hash.hash(password_concat)
            await cur.execute("INSERT INTO Users (name, email, password, role) VALUES(%s, %s, %s, %s)", ("Admin", "admin@mail.com", hash, "ADMIN"))
            # supervisor user
            password = "supervisor123"
            password_concat = password + config["SECRET_KEY_PASS"]
            hash = password_hash.hash(password_concat)
            await cur.execute("INSERT INTO Users (name, email, password, role) VALUES(%s, %s, %s, %s)", ("Supervisor", "supervisor@mail.com", hash, "SUPERVISOR"))
            # staff user
            password = "staff123"
            password_concat = password + config["SECRET_KEY_PASS"]
            hash = password_hash.hash(password_concat)
            await cur.execute("INSERT INTO Users (name, email, password, role) VALUES(%s, %s, %s, %s)", ("Staff", "staff@mail.com", hash, "STAFF"))
            
            
        await conn.commit()
        
        
        
# if __name__ == "__main__":
# Create the compatible loop factory
loop_factory = lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())

# Run using the factory
asyncio.run(CreatedUSer(), loop_factory=loop_factory)