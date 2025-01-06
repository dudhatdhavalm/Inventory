from sqlalchemy.orm import Session
from models.stock import StockDetails
# from schemas.stock_detail import StockDetailsCreate
from sqlalchemy import func
from models.item import Item
from models.inward import InwardItem
from models.outward_return import OutwardReturn
from models.inward_return import InwardReturn


class CRUDStockDetails:
    def create(self, db: Session):
        # Fetch all items from InwardItem and their total inward quantities
        items_query = (
            db.query(
                InwardItem.item_id, func.sum(InwardItem.quantity).label("total_inward")
            )
            .group_by(InwardItem.item_id)
            .all()
        )

        stock_details = []

        for item_id, total_inward in items_query:
            # Fetch total inward returns for the item
            inward_return_query = (
                db.query(func.sum(InwardReturn.quantity))
                .filter(InwardReturn.item_id == item_id)
                .first()
            )
            total_inward_return = (
                inward_return_query[0] if inward_return_query[0] is not None else 0
            )

            # Fetch total outward returns for the item
            outward_return_query = (
                db.query(func.sum(OutwardReturn.quantity))
                .filter(OutwardReturn.item_id == item_id)
                .first()
            )
            total_outward_return = (
                outward_return_query[0] if outward_return_query[0] is not None else 0
            )

            # Calculate available quantity
            available_quantity = (
                total_inward - total_inward_return + total_outward_return
            )

            # Fetch item name
            item_name_query = db.query(Item.name).filter(Item.id == item_id).first()
            item_name = item_name_query[0] if item_name_query else "Unknown Item"

            # Create a new stock record for the item
            db_obj = StockDetails(
                item_id=item_id,  # Use the correct item_id from the query
                quantity=total_inward,
                available_quantity=available_quantity,
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            # Append stock details for the item
            stock_details.append(
                {
                    "item_name": item_name,
                    "quantity": total_inward,
                    "available_quantity": available_quantity,
                }
            )

        return stock_details


stock_details = CRUDStockDetails()
