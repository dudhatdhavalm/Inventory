from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.inward_return import InwardReturn
from models.inward import InwardItem
from schemas.inward_return import InwardReturnCreate


class CRUDInwardReturn:
    def create(self, db: Session, *, obj_in: InwardReturnCreate) -> str:
        inward_item = db.query(InwardItem).filter_by(id=obj_in.inward_item_id).first()
        if not inward_item:
            raise HTTPException(
                status_code=404,
                detail=f"InwardItem with ID {obj_in.inward_item_id} not found.",
            )

        # Validate the quantity
        if inward_item.quantity < obj_in.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient quantity in InwardItem (ID: {obj_in.inward_item_id}). "
                f"Available: {inward_item.quantity}, Requested: {obj_in.quantity}.",
            )

        # Update the quantity in InwardItem table
        inward_item.quantity -= obj_in.quantity
        db.add(inward_item)

        inward_return = InwardReturn(
            item_id=inward_item.item_id,
            inward_id=inward_item.inward_id,
            quantity=obj_in.quantity,
            return_date=datetime.utcnow(),
            return_reason=obj_in.return_reason,
        )
        db.add(inward_return)
        db.commit()

        return "Inward item returned successfully."


inward_return = CRUDInwardReturn()
