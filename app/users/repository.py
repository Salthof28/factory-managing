from app import db_connect
from fastapi import Depends
from psycopg import AsyncConnection
from .models.createUser import CreateUser

class UsersRepository:
    def __init__(self, db: AsyncConnection = Depends(db_connect.con_db)):
        self.db: AsyncConnection = db
    
    
    async def findExistingUser(self, dataString: CreateUser):
        # (phone IS NOT NULL AND phone = %s). if phone not null search phone
        # WHEN email = %s THEN 'email', if email equal datastring.email, result matching 'email'
        # WHEN phone = %s THEN 'phone', if email equal datastring.phone, result matching 'phone'
        query = """
            SELECT id, 
            CASE 
                WHEN email = %s THEN 'email'
                WHEN phone = %s THEN 'phone'
            END as matched_field
            FROM users WHERE email = %s OR (phone IS NOT NULL AND phone = %s)
            LIMIT 1
        """
    
        params = (
            dataString.email, # for CASE WHEN email
            dataString.phone, # for CASE WHEN phone
            dataString.email, # for WHERE email
            dataString.phone, # for WHERE phone (IS NOT NULL & phone =)
        )
        async with self.db.cursor() as cur:
            await cur.execute(query, params)
            data = await cur.fetchone()
            if data:
                return data["matched_field"]
            return None
            
        
    
    async def register(self, newUser: CreateUser):
        async with self.db.cursor() as cur:
            query: str = "INSERT INTO Users (name, email, phone, password, role, img_profile) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *"
            valueData: tuple = (newUser.name, newUser.email, newUser.phone, newUser.password, newUser.role, newUser.img_profile)
            
            await cur.execute(query, valueData)
            data = await cur.fetchone()
            await self.db.commit()
            return data