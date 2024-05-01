from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from db.base_class import Base
from models.permission import Permission
from schemas.permission import PermissionCreate, PermissionUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Permission]:
        return db.query(Permission).filter(Permission.status == 1).offset(skip).limit(limit).all()
            
    def get_by_id(self, db: Session, *, id: int) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.id == id, Permission.status == 1).first()

    def create(self, db: Session, *, obj_in: PermissionCreate, created_by=None) -> Permission:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Permission(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Permission,
        obj_in: Union[Permission, Dict[str, Any]],
        modified_by=None
    ) -> Permission:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(
            db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by
        )



permission = CRUDPermission(Permission)
