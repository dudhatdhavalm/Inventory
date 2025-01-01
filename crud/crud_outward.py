from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi import HTTPException
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models.outward import Outward, OutwardItem
from models.supplier import Supplier
from models.item import Item
from db.base_class import Base
from schemas.outward import OutwardCreate, OutwardUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDOutward(CRUDBase[Outward, OutwardCreate, OutwardUpdate]):
    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Outward]:
        # Fetch the Outward records along with Supplier information
        outwards = (
            db.query(Outward, Supplier.name.label("supplier_name"))
            .join(
                Supplier, Outward.supplier_id == Supplier.id, isouter=True
            )  # Assuming 'supplier_id' is the foreign key
            .filter(Outward.status == 1)
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Extract Outward records and add supplier_name
        outwards_with_supplier = []
        for outward, name in outwards:
            outward.supplier_name = name  # Add the supplier_name to the Outward object
            outwards_with_supplier.append(outward)

        # Fetch related OutwardItems based on the outward_ids
        outward_ids = [outward.id for outward in outwards_with_supplier]
        outward_items = (
            db.query(OutwardItem).filter(OutwardItem.outward_id.in_(outward_ids)).all()
        )

        # Associate OutwardItems with Outward records
        for outward in outwards_with_supplier:
            outward.items = [
                item for item in outward_items if item.outward_id == outward.id
            ]

        return outwards_with_supplier

    def get_by_id(self, db: Session, *, outward_id: int) -> Optional[Outward]:
        outward = (
            db.query(Outward)
            .filter(Outward.id == outward_id, Outward.status == 1)
            .first()
        )

        if not outward:
            return {"detail": "outward not found"}

        supplier = (
            db.query(Supplier.name).filter(Supplier.id == outward.supplier_id).first()
        )

        outward.supplier_name = supplier[0] if supplier else None

        outward_items = (
            db.query(OutwardItem, Item)
            .join(Item, Item.id == OutwardItem.item_id)
            .filter(OutwardItem.outward_id == outward.id)
            .all()
        )

        if not outward_items:
            return {"detail": "No outward items found"}
        outward.items = [
            {
                "item_id": outward_item.item_id,
                "quantity": outward_item.quantity,
                "name": item.name,
                "unit": item.unit,
                "rate": item.rate,
            }
            for outward_item, item in outward_items
        ]

        return {
            "outward_id": outward.id,
            "invoice_no": outward.invoice_no,
            "challan_no": outward.challan_no,
            "gst_no": outward.gst_no,
            "date": outward.date,
            "supplier_name": outward.supplier_name,
            "items": outward.items,
        }

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
            supplier_name=obj_in.supplier_name
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
        outward_id: int,
        obj_in: OutwardUpdate,
        items: List[OutwardItem],  # Here you expect items to be a list from the body
    ) -> Outward:
        outward_data = db.query(Outward).filter(Outward.id == outward_id).first()
        if not outward_data:
            raise HTTPException(status_code=404, detail="Outward not found")

        # Update the main outward record fields
        outward_data.date = obj_in.date
        outward_data.invoice_no = obj_in.invoice_no
        outward_data.challan_no = obj_in.challan_no
        outward_data.gst_no = obj_in.gst_no
        outward_data.supplier_id = obj_in.supplier_id
        outward_data.supplier_name = obj_in.supplier_name

        db.commit()
        db.refresh(outward_data)

        # Delete old outward items associated with this outward_id
        db.query(OutwardItem).filter(OutwardItem.outward_id == outward_id).delete()
        db.commit()

        total_amount = 0
        outward_items = []

        # Add new outward items
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

        # Update the grand total for outward
        outward_data.grand_total = total_amount
        db.commit()

        return outward_data


outward = CRUDOutward(Outward)
