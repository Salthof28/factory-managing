from pydantic import BaseModel

class EnumRoleUser(BaseModel):
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    STAFF = "STAFF"