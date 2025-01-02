from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from schemas.item import ItemBase


class InwardBase(BaseModel):
    date: Optional[datetime] = None
    invoice_no: Optional[str] = None
    challan_no: Optional[str] = None
    gst_no: Optional[str] = None
    supplier_id: Optional[int] = None

    class Config:
        orm_mode = True


class InwardItemBase(BaseModel):
    item_id: int
    name: str
    quantity: int
    unit: str
    rate: int
    total_price: Optional[int] = None 

    class Config:
        orm_mode = True


class InwardCreate(InwardBase):
    items: List[InwardItemBase]

    class Config:
        orm_mode = True


class InwardUpdate(InwardBase):
    items: List[InwardItemBase]


class InwardDelete(InwardBase):
    id: int


class InwardInDBBase(InwardBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class InwardOnly(InwardInDBBase): ...


class InwardSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool
