from enum import Enum

class EnumRoleUser(str, Enum):
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    STAFF = "STAFF"