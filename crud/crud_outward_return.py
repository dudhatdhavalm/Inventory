from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.outward_return import OutwardReturn
from models.outward import OutwardItem
from schemas.outward_return import OutwardReturnCreate


class CRUDOutwardReturn:
    def create(self, db: Session, *, obj_in: OutwardReturnCreate) -> str:
        print(f"Received outward_item_id: {obj_in.outward_item_id}")

        # Fetch OutwardItem record
        outward_item = (
            db.query(OutwardItem)
            .filter(OutwardItem.id == obj_in.outward_item_id)
            .first()
        )
        if not outward_item:
            print(
                f"OutwardItem with ID {obj_in.outward_item_id} not found in the database."
            )
            raise HTTPException(
                status_code=404,
                detail=f"OutwardItem with ID {obj_in.outward_item_id} not found.",
            )

        print(f"OutwardItem found: {outward_item}")

        # Check for sufficient quantity
        if outward_item.quantity < obj_in.quantity:
            print(
                f"Insufficient quantity: Available={outward_item.quantity}, Requested={obj_in.quantity}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient quantity in OutwardItem (ID: {obj_in.outward_item_id}). "
                f"Available: {outward_item.quantity}, Requested: {obj_in.quantity}.",
            )

        # Update quantity
        outward_item.quantity -= obj_in.quantity
        db.add(outward_item)

        # Create OutwardReturn record
        outward_return = OutwardReturn(
            item_id=outward_item.item_id,
            outward_id=outward_item.outward_id,
            quantity=obj_in.quantity,
            return_date=datetime.utcnow(),
            return_reason=obj_in.return_reason,
        )
        db.add(outward_return)
        db.commit()

        print(f"OutwardReturn created successfully: {outward_return}")
        return "Outward item returned successfully."


outward_return = CRUDOutwardReturn()
