from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from api import dependencies
from schemas.inward_return import InwardReturnCreate, InwardReturnResponse

router = APIRouter()


@router.post("/return", response_model=InwardReturnResponse, status_code=201)
def return_inward_item(
    *, db: Session = Depends(dependencies.get_db), obj_in: InwardReturnCreate
):
    """
    Endpoint to return inward items based on inwarditem_id.
    """
    message = crud.inward_return.create(db=db, obj_in=obj_in)
    return {"message": message}

