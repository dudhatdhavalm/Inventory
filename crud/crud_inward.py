from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.inward import Inward
from db.base_class import Base
from schemas.inward import InwardCreate, InwardUpdate
ModelType = TypeVar("ModelType", bound=Base)


class CRUDInward(CRUDBase[Inward, InwardCreate, InwardUpdate]):
    def get(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Inward]:
        return db.query(Inward).filter(Inward.status == 1).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, *, id: int) -> Optional[Inward]:
        return db.query(Inward).filter(Inward.id == id,Inward.status == 1).first()

    def get_by_supplier_id(self, db: Session, *, id: int) -> Optional[Inward]:
        return db.query(Inward).filter(Inward.supplier_id == id,Inward.status == 1).first()

    def get_by_type(self, db: Session, *, type: str) -> List[Inward]:
        return db.query(Inward).filter(Inward.type == type,Inward.status == 1).all()

    def create(self, db: Session, *, obj_in: InwardCreate, created_by=None) -> Inward:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Inward(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Inward, obj_in: Union[Inward, Dict[str, Any]], modified_by=None
    ) -> Inward:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)


inward = CRUDInward(Inward)
