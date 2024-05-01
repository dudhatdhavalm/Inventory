from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class PermissionBase(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None


class PermissionCreate(PermissionBase):
    ...

    class Config:
        orm_mode = True


class PermissionUpdate(PermissionBase):
    id: int


class PermissionDelete(PermissionBase):
    id: int


class PermissionInDBBase(PermissionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class PermissionOnly(PermissionInDBBase): 
    ...


class PermissionSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool
    name: Optional[str]

class PermissionSearchResults(PermissionSearch):
    items: List[PermissionOnly] = []