from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class ItemBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    gst: Optional[str] = None
    rate: Optional[str] = None
    unit: Optional[str] = None
    cost_rate: Optional[int] = None
    final_rate: Optional[int] = None


class ItemCreate(ItemBase):
    ...

    class Config:
        orm_mode = True


class ItemUpdate(ItemBase):
    id: int


class ItemDelete(ItemBase):
    id: int


class ItemInDBBase(ItemBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class ItemOnly(ItemInDBBase): ...


class ItemSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool
