from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.inward import Inward, InwardItem
from models.item import Item
from db.base_class import Base
from schemas.inward import InwardCreate, InwardUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDInward(CRUDBase[Inward, InwardCreate, InwardUpdate]):
    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Inward]:
        return (
            db.query(Inward).filter(Inward.status == 1).offset(skip).limit(limit).all()
        )

    def get_by_id(self, db: Session, *, id: int) -> Optional[Inward]:
        return db.query(Inward).filter(Inward.id == id, Inward.status == 1).first()

    def get_by_supplier_id(self, db: Session, *, id: int) -> Optional[Inward]:
        return (
            db.query(Inward)
            .filter(Inward.supplier_id == id, Inward.status == 1)
            .first()
        )

    def get_by_type(self, db: Session, *, type: str) -> List[Inward]:
        return db.query(Inward).filter(Inward.type == type, Inward.status == 1).all()

    def create(
        self,
        db: Session,
        *,
        obj_in: InwardCreate,
        items: List[InwardItem],
    ) -> Inward:
        inward_data = Inward(
            date=obj_in.date,
            invoice_no=obj_in.invoice_no,
            grand_total=0,
            challan_no=obj_in.challan_no,
            gst_no=obj_in.gst_no,
            supplier_id=obj_in.supplier_id,
        )

        db.add(inward_data)
        db.commit()
        db.refresh(inward_data)

        total_amount = 0 
        inward_items = []

        for item in items:
            total_price = item.rate * item.quantity 
            total_amount += total_price

            inward_item = InwardItem(
                inward_id=inward_data.id,
                item_id=item.item_id,
                name=item.name,
                quantity=item.quantity,
                unit=item.unit,
                rate=item.rate,
                total_price=total_price,
            )
            inward_items.append(inward_item)

        db.add_all(inward_items)
        db.commit()

        inward_data.grand_total = total_amount 
        db.commit()

        return inward_data

    def update(
        self,
        db: Session,
        *,
        db_obj: Inward,
        obj_in: Union[Inward, Dict[str, Any]],
        modified_by=None,
    ) -> Inward:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(
            db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by
        )


inward = CRUDInward(Inward)
