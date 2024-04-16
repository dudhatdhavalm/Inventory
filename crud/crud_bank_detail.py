from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.security import get_password_hash
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.bank_detail import BankDetail
from db.base_class import Base
from schemas.bank_detail import BankDetailCreate, BankDetailUpdate
ModelType = TypeVar("ModelType", bound=Base)


class CRUDBankDetail(CRUDBase[BankDetail, BankDetailCreate, BankDetailUpdate]):
    def get(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[BankDetail]:
        return db.query(BankDetail).filter(BankDetail.status == 1).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, *, id: int) -> Optional[BankDetail]:
        return db.query(BankDetail).filter(BankDetail.id == id,BankDetail.status == 1).first()

    def get_by_supplier_id(self, db: Session, *, id: int) -> Optional[BankDetail]:
        return db.query(BankDetail).filter(BankDetail.supplier_id == id,BankDetail.status == 1).first()

    def create(self, db: Session, *, obj_in: BankDetailCreate, created_by=None) -> BankDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = BankDetail(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: BankDetail, obj_in: Union[BankDetail, Dict[str, Any]], modified_by=None
    ) -> BankDetail:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)




bank_detail = CRUDBankDetail(BankDetail)
