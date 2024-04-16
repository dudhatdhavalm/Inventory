from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.security import get_password_hash
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.contact_detail import ContactDetail
from db.base_class import Base
from schemas.contact_detail import ContactDetailCreate, ContactDetailUpdate
ModelType = TypeVar("ModelType", bound=Base)


class CRUDContactDetail(CRUDBase[ContactDetail, ContactDetailCreate, ContactDetailUpdate]):
    def get(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ContactDetail]:
        return db.query(ContactDetail).filter(ContactDetail.status == 1).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, *, id: int) -> Optional[ContactDetail]:
        return db.query(ContactDetail).filter(ContactDetail.id == id,ContactDetail.status == 1).first()

    def get_by_supplier_id(self, db: Session, *, id: int) -> Optional[ContactDetail]:
        return db.query(ContactDetail).filter(ContactDetail.supplier_id == id,ContactDetail.status == 1).first()

    def create(self, db: Session, *, obj_in: ContactDetailCreate, created_by=None) -> ContactDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = ContactDetail(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ContactDetail, obj_in: Union[ContactDetail, Dict[str, Any]], modified_by=None
    ) -> ContactDetail:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)


contact_detail = CRUDContactDetail(ContactDetail)
