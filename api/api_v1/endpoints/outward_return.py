from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from api import dependencies
from schemas.outward_return import OutwardReturnCreate, OutwardReturnResponse

router = APIRouter()


@router.post("/return", response_model=OutwardReturnResponse, status_code=201)
def return_outward_item(
    *, db: Session = Depends(dependencies.get_db), obj_in: OutwardReturnCreate
):
    """
    Endpoint to return inward items based on inwarditem_id.
    """
    message = crud.outward_return.create(db=db, obj_in=obj_in)
    return {"message": message}
