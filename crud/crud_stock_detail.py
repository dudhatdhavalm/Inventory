from sqlalchemy.orm import Session
from models.stock import StockDetails
from schemas.stock_detail import StockDetailsCreate
from sqlalchemy import func
from models.item import Item
from models.inward import InwardItem
from models.outward_return import OutwardReturn
from models.inward_return import InwardReturn


class CRUDStockDetails:
    def create(self, db: Session, obj_in: StockDetailsCreate):
        total_inward_query = (
            db.query(func.sum(InwardItem.quantity))
            .filter(InwardItem.item_id == obj_in.item_id)
            .first()
        )
        total_inward = total_inward_query[0] if total_inward_query[0] is not None else 0

        inward_return_query = (
            db.query(func.sum(InwardReturn.quantity))
            .filter(InwardReturn.item_id == obj_in.item_id)
            .first()
        )
        total_inward_return = (
            inward_return_query[0] if inward_return_query[0] is not None else 0
        )

        total_outward_query = (
            db.query(func.sum(OutwardReturn.quantity))
            .filter(OutwardReturn.item_id == obj_in.item_id)
            .first()
        )
        total_outward = (
            total_outward_query[0] if total_outward_query[0] is not None else 0
        )

        available_quantity = total_inward + total_outward - total_inward_return

        item_name_query = db.query(Item.name).filter(Item.id == obj_in.item_id).first()
        item_name = item_name_query[0] if item_name_query else "Unknown Item"

        db_obj = StockDetails(
            item_id=obj_in.item_id,
            quantity=total_inward,
            available_quantity=available_quantity,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Return only the required fields
        return {
            "item_name": item_name,
            "quantity": db_obj.quantity,
            "available_quantity": db_obj.available_quantity,
        }


stock_details = CRUDStockDetails()
