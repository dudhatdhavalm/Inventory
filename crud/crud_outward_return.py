from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.outward_return import OutwardReturn
from models.outward import OutwardItem
from schemas.outward_return import OutwardReturnCreate

class CRUDOutwardReturn:
    def create(self, db: Session, *, obj_in: OutwardReturnCreate) -> str:
        outward_item = db.query(OutwardItem).filter_by(id=obj_in.outward_item_id).first()
        if not outward_item:
            raise HTTPException(
                status_code=404,
                detail=f"InwardItem with ID {obj_in.outward_item_id} not found.",
            )

        # Validate the quantity
        if outward_item.quantity < obj_in.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient quantity in InwardItem (ID: {obj_in.outward_item_id}). "
                f"Available: {outward_item.quantity}, Requested: {obj_in.quantity}.",
            )

        # Update the quantity in InwardItem table
        outward_item.quantity -= obj_in.quantity
        db.add(outward_item)

        outward_return = OutwardReturn(
            item_id=outward_item.item_id,
            inward_id=outward_item.outward_id,
            quantity=obj_in.quantity,
            return_date=datetime.utcnow(),
            return_reason=obj_in.return_reason,
        )
        db.add(outward_return)
        db.commit()

        return "Inward item returned successfully."


outward_return = CRUDOutwardReturn()
