from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class SupplierBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    distance: Optional[str] = None
    station: Optional[str] = None
    transport: Optional[str] = None


class SupplierCreate(SupplierBase):
    ...

    class Config:
        orm_mode = True


class SupplierUpdate(SupplierBase):
    id: int


class SupplierDelete(SupplierBase):
    id: int


class SupplierInDBBase(SupplierBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class SupplierOnly(SupplierInDBBase): ...


class SupplierSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool


class SupplierBankContactSchema(SupplierBase):
    id: int
    account_no: Optional[str] = None
    branch: Optional[str] = None
    IFSC_code: Optional[str] = None
    bank: Optional[str] = None
    contact_name: Optional[str] = None
    mobile_number: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    pan_no: Optional[str] = None
    gstin: Optional[str] = None