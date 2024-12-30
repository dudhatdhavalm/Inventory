from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class OutwardBase(BaseModel):
    date: Optional[datetime] = None
    invoice_no: Optional[str] = None
    challan_no: Optional[str] = None
    gst_no: Optional[str] = None
    supplier_id: Optional[int] = None

    class Config:
        orm_mode = True


class OutwardItemBase(BaseModel):
    item_id: int
    name: str
    quantity: int
    unit: str
    rate: int

    class Config:
        orm_mode = True


class OutwardCreate(OutwardBase):
    items: List[OutwardItemBase]

    class Config:
        orm_mode = True


class OutwardUpdate(OutwardBase):
    items: List[OutwardItemBase]


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
