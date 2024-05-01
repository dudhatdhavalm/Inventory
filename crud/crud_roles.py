from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from db.base_class import Base
from models.roles import Roles
from schemas.roles import RolesCreate, RolesUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDRoles(CRUDBase[Roles, RolesCreate, RolesUpdate]):
    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Roles]:
        return db.query(Roles).filter(Roles.status == 1).offset(skip).limit(limit).all()
            
    def get_by_id(self, db: Session, *, id: int) -> Optional[Roles]:
        return db.query(Roles).filter(Roles.id == id, Roles.status == 1).first()

    def create(self, db: Session, *, obj_in: RolesCreate, created_by=None) -> Roles:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Roles(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Roles,
        obj_in: Union[Roles, Dict[str, Any]],
        modified_by=None
    ) -> Roles:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(
            db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by
        )



roles = CRUDRoles(Roles)
