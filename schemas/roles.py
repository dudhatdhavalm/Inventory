from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class RolesBase(BaseModel):
    name: Optional[str] = None
    status:  Optional[int] = 1

class RolesCreate(RolesBase):
    ...

    class Config:
        orm_mode = True


class RolesUpdate(RolesBase):
    id: int


class RolesDelete(RolesBase):
    id: int


class RolesInDBBase(RolesBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RolesOnly(RolesInDBBase): 
    ...


class RolesSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool
    name: Optional[str]

class RolesSearchResults(RolesSearch):
    items: List[RolesOnly] = []