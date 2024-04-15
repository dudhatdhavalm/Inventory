from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class ContactDetailBase(BaseModel):
    contact_name: Optional[str] = None
    mobile_number: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    pan_no: Optional[str] = None
    gstin: Optional[str] = None


class ContactDetailCreate(ContactDetailBase):
    supplier_id: int
    class Config:
        orm_mode = True


class ContactDetailUpdate(ContactDetailBase):
    id: int


class ContactDetailDelete(ContactDetailBase):
    id: int


class ContactDetailInDBBase(ContactDetailBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class ContactDetailOnly(ContactDetailInDBBase): 
    ...


class ContactDetailSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool
