import psycopg
from dotenv import dotenv_values

config = dotenv_values(".env")

with psycopg.connect(f"dbname={config["DB_NAME"]} user={config["USER"]} password={config["PASSWORD"]} host={config["HOST"]}") as conn:
    
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE Warehouse (
                    id serial PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    price DECIMAL(17, 2) NOT NULL,
                    stock INTEGER NOT NULL,
                    description TEXT NULL)  
                """)
        
        cur.execute("INSERT INTO Warehouse (name, price, stock, description) VALUES(%s, %s, %s, %s)", ("Spoiler Supra", 8500000, 5, "This is spoiler for improve looking supra cars"))
        cur.execute("INSERT INTO Warehouse (name, price, stock, description) VALUES(%s, %s, %s, %s)", ("LED Front", 2500000, 50, "Lamp car front for improve sight in night"))
        
        cur.execute("SELECT * FROM Warehouse")
        print(cur.fetchall())
        
    conn.commit()