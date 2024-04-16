from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from models.user import User
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from schemas.inward import InwardCreate, InwardOnly, InwardUpdate
from util.user_util import get_current_user

router = APIRouter()


@router.get("", status_code=200)
def fetch_all_inward(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all inward detail
    """
    inward = crud.inward.get(db=db)
    return inward


@router.get("/{inward_id}", status_code=200)
def fetch_inward_id(
    *,
    inward_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch inward by id
    """
    inward = crud.inward.get_by_id(db=db, id=inward_id)
    if not inward:
        raise HTTPException(
            status_code=404, detail=f"Inward with ID {inward_id} not found"
        )
    return inward

@router.get("/{supplier_id}/supplier", status_code=200)
def fetch_by_supplier_id(
    *,
    supplier_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch inward by supplier id
    """
    inward = crud.inward.get_by_supplier_id(db=db, id=supplier_id)
    if not inward:
        raise HTTPException(
            status_code=404,
            detail=f"Supplier with ID {supplier_id} not found",
        )
    return inward



@router.get("/", status_code=200)
def fetch_by_type(
    *,
    type: str,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch detail by type
    """
    inward = crud.inward.get_by_type(db=db, type=type)

    return inward

@router.post("", status_code=200)
def add_inward(
    *, inward_in: InwardCreate, db: Session = Depends(dependencies.get_db)
):
    inward = crud.inward.create(db=db, obj_in=inward_in)
    return inward


@router.put("/{inward_id}", status_code=200, response_model=InwardOnly)
def update_inward(
    *,
    request: Request,
    inward_id: int,
    inward_in: InwardUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update Inward Detail
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    inward_record = crud.inward.get_by_id(db=db,id=inward_in.id)
     
    if not inward_record :
        raise HTTPException(
            status_code=404, detail=f"Inward not found with this id"
        )

    result = crud.inward.get_by_id(db=db, id=inward_id)
    inward = crud.inward.update(
        db=db, db_obj=result, obj_in=inward_in, modified_by=modified_by
    )

    return inward


@router.delete("/{inward_id}", status_code=200)
def delete_inward(
    *, inward_id: int, db: Session = Depends(dependencies.get_db)
):
    """
    Delete inward
    """
    result = crud.inward.get_by_id(db=db, id=inward_id)
    
    print(result)
    result.status = 0
    db.commit()

    return "inward Deleted successfully"
