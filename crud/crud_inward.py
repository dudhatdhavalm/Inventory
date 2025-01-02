from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.inward import Inward, InwardItem
from models.supplier import Supplier
from models.item import Item
from db.base_class import Base
from schemas.inward import InwardCreate, InwardUpdate
from sqlalchemy.orm import joinedload

ModelType = TypeVar("ModelType", bound=Base)


class CRUDInward(CRUDBase[Inward, InwardCreate, InwardUpdate]):
    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Inward]:
        inwards = (
            db.query(Inward, Supplier.name.label("supplier_name"))
            .join(Supplier, Inward.supplier_id == Supplier.id, isouter=True)
            .filter(Inward.status == 1)
            .offset(skip)
            .limit(limit)
            .all()
        )

        inwards_with_supplier = []
        for inward, name in inwards:
            inward.supplier_name = name
            inwards_with_supplier.append(inward)

        inward_ids = [inward.id for inward in inwards_with_supplier]
        inward_items = (
            db.query(InwardItem).filter(InwardItem.inward_id.in_(inward_ids)).all()
        )

        for inward in inwards_with_supplier:
            inward.items = [
                item for item in inward_items if item.inward_id == inward.id
            ]

        return inwards_with_supplier

    def delete_by_id(self, db: Session, *, inward_id: int):
        inward = (
            db.query(Inward).filter(Inward.id == inward_id, Inward.status == 1).first()
        )
        print(f"Queried inward for ID {inward_id}: {inward}")

        if not inward:
            return {"detail": "Inward not found"}

        inward.status = 0
        db.commit()
        db.refresh(inward)
        return {
            "inward_id": inward.id,
            "message": "Inward status updated to 0 (soft deleted)",
        }

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
        inward_id: int,
        obj_in: InwardCreate,
        items: List[InwardItem],
    ) -> Inward:
        inward_data = db.query(Inward).filter(Inward.id == inward_id).first()
        if not inward_data:
            raise HTTPException(status_code=404, detail="Inward not found")

        inward_data.date = obj_in.date
        inward_data.invoice_no = obj_in.invoice_no
        inward_data.challan_no = obj_in.challan_no
        inward_data.gst_no = obj_in.gst_no
        inward_data.supplier_id = obj_in.supplier_id

        db.commit()
        db.refresh(inward_data)

        db.query(InwardItem).filter(InwardItem.inward_id == inward_id).delete()
        db.commit()

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

    def get_items_by_supplier_id(self, db: Session, supplier_id: int) -> List[Dict]:
        inward_records = (
            db.query(Inward).filter(Inward.supplier_id == supplier_id).all()
        )
        if not inward_records:
            return []

        inward_ids = [record.id for record in inward_records]

        inward_items = (
            db.query(InwardItem).filter(InwardItem.inward_id.in_(inward_ids)).all()
        )
        if not inward_items:
            return []

        item_ids = [item.item_id for item in inward_items]

        items = db.query(Item).filter(Item.id.in_(item_ids)).all()
        if not items:
            return []

        return [
            {
                "item_id": item.id,
                "inward_id": inward_item.inward_id,
                "name": item.name,
                "type": item.type,
                "gst": item.gst,
                "rate": item.rate,
                "unit": item.unit,
                "cost_rate": item.cost_rate,
            }
            for item in items
            for inward_item in inward_items
            if inward_item.item_id == item.id
        ]


inward = CRUDInward(Inward)
