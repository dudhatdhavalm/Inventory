from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.security import get_password_hash
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.bank_detail import BankDetail
from models.contact_detail import ContactDetail
from models.supplier import Supplier
from db.base_class import Base
from schemas.supplier import SupplierCreate, SupplierUpdate
ModelType = TypeVar("ModelType", bound=Base)


class CRUDSupplier(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    def get(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Supplier]:
        return db.query(Supplier).filter(Supplier.status == 1).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, *, id: int) -> Optional[Supplier]:
        return db.query(Supplier).filter(Supplier.id == id).first()

    # def get_by_bank_contact_id(self, db: Session, *, id: int):
    #     obj = db.query(Supplier.id,Supplier.name,Supplier.address,Supplier.city,Supplier.distance,Supplier.pincode,Supplier.station,Supplier.transport,BankDetail.IFSC_code,BankDetail.account_no,BankDetail.branch,BankDetail.bank,ContactDetail.contact_name,ContactDetail.mobile_number,ContactDetail.phone_number,ContactDetail.email,ContactDetail.pan_no,ContactDetail.gstin).join(BankDetail,BankDetail.supplier_id == Supplier.id).join(ContactDetail,ContactDetail.supplier_id == Supplier.id).filter(
    #             Supplier.id == id
    #             ).first()
    #     return obj

    def get_by_bank_contact_id(self, db: Session, *, id: int):
        obj = db.query(Supplier.id,Supplier.name,Supplier.address,Supplier.city,Supplier.distance,Supplier.pincode,Supplier.station,Supplier.transport,BankDetail.IFSC_code,BankDetail.account_no,BankDetail.branch,BankDetail.bank,ContactDetail.contact_name,ContactDetail.mobile_number).join(BankDetail,BankDetail.supplier_id == Supplier.id).filter(
                Supplier.id == id
                ).first()
        return obj

    
    def create(self, db: Session, *, obj_in: SupplierCreate, created_by=None) -> Supplier:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Supplier(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Supplier, obj_in: Union[Supplier, Dict[str, Any]], modified_by=None
    ) -> Supplier:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)




supplier = CRUDSupplier(Supplier)
