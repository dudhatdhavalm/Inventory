from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

from schemas.roles import RolesInDBBase, RolesOnly


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: int = 1
    gender: Optional[str] = None


class UserCreate(UserBase):
    first_name: str
    email: EmailStr
    status: int = 1
    class Config:
        orm_mode = True

class UserDetails(UserBase):
    gender: str
    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    id: int


class UserDelete(UserBase):
    id: int


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class User(UserInDBBase):
    ...
    roles: List[RolesOnly] = []

class UserRoleAssignment(BaseModel):
    role_id: int

class UserRole(BaseModel):
    roles: List[RolesInDBBase] = []

    class Config:
        orm_mode = True    
        
class UserOnly(UserInDBBase):
    ...


class UserSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool

