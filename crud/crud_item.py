from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.item import Item
from db.base_class import Base
from schemas.item import ItemCreate, ItemUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get(self, db: Session, *, skip: int = 0, limit: int = 100,name: str=None) -> List[Item]:
        print(name)
        if name is None:
            return db.query(Item).filter(Item.status == 1).offset(skip).limit(limit).all()
        else:
            return db.query(Item).filter(Item.name.ilike(f"%{name}%"),Item.status == 1).offset(skip).limit(limit).all()
            
    def get_by_id(self, db: Session, *, id: int) -> Optional[Item]:
        return db.query(Item).filter(Item.id == id, Item.status == 1).first()

    def create(self, db: Session, *, obj_in: ItemCreate, created_by=None) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Item(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Item,
        obj_in: Union[Item, Dict[str, Any]],
        modified_by=None
    ) -> Item:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(
            db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by
        )


item = CRUDItem(Item)
