from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from models.user import User
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from schemas.outward import OutwardCreate, OutwardOnly, OutwardUpdate
from util.user_util import get_current_user

router = APIRouter()


@router.get("", status_code=200)
def fetch_all_outward(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all outward detail
    """
    outward = crud.outward.get(db=db)
    return outward


@router.get("/{outward_id}", status_code=200)
def fetch_outward_id(
    *,
    outward_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch outward by id
    """
    outward = crud.outward.get_by_id(db=db, id=outward_id)
    if not outward:
        raise HTTPException(
            status_code=404, detail=f"Outward with ID {outward_id} not found"
        )
    return outward

@router.get("/{supplier_id}/supplier", status_code=200)
def fetch_by_supplier_id(
    *,
    supplier_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch outward by supplier id
    """
    outward = crud.outward.get_by_supplier_id(db=db, id=supplier_id)
    if not outward:
        raise HTTPException(
            status_code=404,
            detail=f"Supplier with ID {supplier_id} not found",
        )
    return outward


@router.post("", status_code=200)
def add_outward(
    *, outward_in: OutwardCreate, db: Session = Depends(dependencies.get_db)
):
    outward = crud.outward.create(db=db, obj_in=outward_in)
    return outward


@router.put("/{outward_id}", status_code=200, response_model=OutwardOnly)
def update_outward(
    *,
    request: Request,
    outward_id: int,
    outward_in: OutwardUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update Outward Detail
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    outward_record = crud.outward.get_by_id(db=db,id=outward_in.id)
     
    if not outward_record :
        raise HTTPException(
            status_code=404, detail=f"Outward not found with this id"
        )

    result = crud.outward.get_by_id(db=db, id=outward_id)
    outward = crud.outward.update(
        db=db, db_obj=result, obj_in=outward_in, modified_by=modified_by
    )

    return outward


@router.delete("/{outward_id}", status_code=200)
def delete_outward(
    *, outward_id: int, db: Session = Depends(dependencies.get_db)
):
    """
    Delete outward
    """
    result = crud.outward.get_by_id(db=db, id=outward_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Outward with ID {outward_id} not found",
        )
    result.status = 0
    db.commit()

    return "Outward Deleted successfully"
