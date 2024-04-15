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
        supplier_data = db.query(Supplier.id,Supplier.name,Supplier.address,Supplier.city,Supplier.distance,Supplier.pincode,Supplier.station,Supplier.transport).filter(
                Supplier.id == id
                ).first()
        
        bank_detail = bank_detail = db.query(BankDetail.IFSC_code,BankDetail.account_no,BankDetail.branch,BankDetail.bank).filter(
                BankDetail.supplier_id == id
                ).first()

        contact_detail = contact_detail = db.query(ContactDetail.contact_name,ContactDetail.mobile_number,ContactDetail.phone_number,ContactDetail.email,ContactDetail.pan_no,ContactDetail.gstin).filter(
                ContactDetail.supplier_id == id
                ).first()
                
        supplier_dict = {
            "id": supplier_data.id,
            "name": supplier_data.name,
            "address": supplier_data.address,
            "city": supplier_data.city,
            "distance": supplier_data.distance,
            "pincode": supplier_data.pincode,
            "station": supplier_data.station,
            "transport": supplier_data.transport,
            "account_no": bank_detail.account_no if bank_detail else None,
            "branch": bank_detail.branch if bank_detail else None,
            "IFSC_code": bank_detail.IFSC_code if bank_detail else None,
            "bank": bank_detail.bank if bank_detail else None,
            "contact_name": contact_detail.contact_name if contact_detail else None,
            "mobile_number": contact_detail.mobile_number if contact_detail else None,
            "phone_number": contact_detail.phone_number if contact_detail else None,
            "email": contact_detail.email if contact_detail else None,
            "pan_no": contact_detail.pan_no if contact_detail else None,
            "gstin": contact_detail.gstin if contact_detail else None,
        }

        return supplier_dict
    
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
