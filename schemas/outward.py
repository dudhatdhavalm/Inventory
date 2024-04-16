from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class OutwardBase(BaseModel):
    date: Optional[datetime] = None
    rate: Optional[int] = None
    invoice_no: Optional[str] = None
    quantity: Optional[int] = None
    grand_total: Optional[int] = None
    challan_no: Optional[str] = None
    gst_no: Optional[str] = None
    supplier_id: Optional[int] = None
    item_id: Optional[int] = None

class OutwardCreate(OutwardBase):
    ...

    class Config:
        orm_mode = True


class OutwardUpdate(OutwardBase):
    id: int


class OutwardDelete(OutwardBase):
    id: int


class OutwardInDBBase(OutwardBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class OutwardOnly(OutwardInDBBase): ...


class OutwardSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool
