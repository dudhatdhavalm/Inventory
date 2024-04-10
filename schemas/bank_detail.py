from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class BankDetailBase(BaseModel):
    account_no: Optional[str] = None
    branch: Optional[str] = None
    IFSC_code: Optional[str] = None
    bank: Optional[str] = None


class BankDetailCreate(BankDetailBase):
    supplier_id: int
    class Config:
        orm_mode = True


class BankDetailUpdate(BankDetailBase):
    id: int


class BankDetailDelete(BankDetailBase):
    id: int


class BankDetailInDBBase(BankDetailBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class BankDetailOnly(BankDetailInDBBase): ...


class BankDetailSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool
