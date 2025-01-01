from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from core.permission_checker import PermissionChecker
from models.user import User
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from schemas.outward import OutwardCreate, OutwardOnly, OutwardUpdate
from util.user_util import get_current_user

router = APIRouter()


@router.get(
    "",
    status_code=200,
    dependencies=[Depends(PermissionChecker(permission="read_outward"))],
)
def fetch_all_outward(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all outward detail
    """
    outward = crud.outward.get(db=db)
    return outward


@router.get(
    "/{outward_id}",
    status_code=200,
    dependencies=[Depends(PermissionChecker(permission="read_outward"))],
)
def fetch_outward_id(
    *,
    outward_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch outward by id
    """
    outward = crud.outward.get_by_id(db=db, outward_id=outward_id)
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


@router.post(
    "",
    status_code=200,
    dependencies=[Depends(PermissionChecker(permission="add_outward"))],
)
def add_outward(
    *, outward_in: OutwardCreate, db: Session = Depends(dependencies.get_db)
):
    try:
        outward = crud.outward.create(db=db, obj_in=outward_in, items=outward_in.items)
        return outward
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/{outward_id}",
    status_code=200,
    response_model=OutwardOnly,
    dependencies=[Depends(PermissionChecker(permission="update_outward"))],
)
def update_outward(
    outward_id: int,
    outward_in: OutwardUpdate,
    db: Session = Depends(dependencies.get_db),
):
    """
    Update Outward Detail
    """
    try:
        outward = crud.outward.update(
            db=db, outward_id=outward_id, obj_in=outward_in, items=outward_in.items
        )
        return outward
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{outward_id}",
    status_code=200,
    dependencies=[Depends(PermissionChecker(permission="delete_outward"))],
)
def delete_outward(*, outward_id: int, db: Session = Depends(dependencies.get_db)):
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
