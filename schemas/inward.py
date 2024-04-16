from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class InwardBase(BaseModel):
    date: Optional[datetime] = None
    rate: Optional[int] = None
    invoice_no: Optional[str] = None
    quantity: Optional[int] = None
    grand_total: Optional[int] = None
    challan_no: Optional[str] = None
    gst_no: Optional[str] = None
    type : Optional[str] = None
    supplier_id: Optional[int] = None
    item_id: Optional[int] = None

class InwardCreate(InwardBase):
    ...

    class Config:
        orm_mode = True


class InwardUpdate(InwardBase):
    id: int


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
