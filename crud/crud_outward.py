from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.outward import Outward
from db.base_class import Base
from schemas.outward import OutwardCreate, OutwardUpdate
ModelType = TypeVar("ModelType", bound=Base)


class CRUDOutward(CRUDBase[Outward, OutwardCreate, OutwardUpdate]):
    def get(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Outward]:
        return db.query(Outward).filter(Outward.status == 1).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, *, id: int) -> Optional[Outward]:
        return db.query(Outward).filter(Outward.id == id,Outward.status == 1).first()

    def get_by_supplier_id(self, db: Session, *, id: int) -> Optional[Outward]:
        return db.query(Outward).filter(Outward.supplier_id == id,Outward.status == 1).first()

    def create(self, db: Session, *, obj_in: OutwardCreate, created_by=None) -> Outward:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Outward(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Outward, obj_in: Union[Outward, Dict[str, Any]], modified_by=None
    ) -> Outward:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)


outward = CRUDOutward(Outward)
