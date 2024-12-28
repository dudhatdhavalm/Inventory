from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.outward import Outward, OutwardItem
from db.base_class import Base
from schemas.outward import OutwardCreate, OutwardUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDOutward(CRUDBase[Outward, OutwardCreate, OutwardUpdate]):
    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Outward]:
        return (
            db.query(Outward)
            .filter(Outward.status == 1)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, *, id: int) -> Optional[Outward]:
        return db.query(Outward).filter(Outward.id == id, Outward.status == 1).first()

    def get_by_supplier_id(self, db: Session, *, id: int) -> Optional[Outward]:
        return (
            db.query(Outward)
            .filter(Outward.supplier_id == id, Outward.status == 1)
            .first()
        )

    def create(
        self,
        db: Session,
        *,
        obj_in: OutwardCreate,
        items: List[OutwardItem],
    ) -> Outward:
        outward_data = Outward(
            date=obj_in.date,
            invoice_no=obj_in.invoice_no,
            challan_no=obj_in.challan_no,
            gst_no=obj_in.gst_no,
            supplier_id=obj_in.supplier_id,
        )

        db.add(outward_data)
        db.commit()
        db.refresh(outward_data)

        total_amount = 0
        outward_items = []

        for item in items:
            total_price = item.rate * item.quantity
            total_amount += total_price

            outward_item = OutwardItem(
                outward_id=outward_data.id,
                item_id=item.item_id,
                name=item.name,
                quantity=item.quantity,
                unit=item.unit,
                rate=item.rate,
                total_price=total_price,
            )
            outward_items.append(outward_item)

        db.add_all(outward_items)
        db.commit()

        outward_data.grand_total = total_amount
        db.commit()

        return outward_data

    def update(
        self,
        db: Session,
        *,
        db_obj: Outward,
        obj_in: Union[Outward, Dict[str, Any]],
        modified_by=None
    ) -> Outward:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(
            db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by
        )


outward = CRUDOutward(Outward)
