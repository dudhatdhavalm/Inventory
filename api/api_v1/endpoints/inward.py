from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from core.permission_checker import PermissionChecker
from models.user import User
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from schemas.inward import InwardCreate, InwardOnly, InwardUpdate
from util.user_util import get_current_user

router = APIRouter()


@router.get(
    "",
    status_code=200,
    dependencies=[Depends(PermissionChecker(permission="display_inward"))],
)
def fetch_all_inward(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all inward detail
    """
    inward = crud.inward.get(db=db)
    return inward


@router.get(
    "/{inward_id}",
    status_code=200,
    dependencies=[Depends(PermissionChecker(permission="display_inward"))],
)
def fetch_inward_id(
    *,
    inward_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch inward by id
    """
    inward = crud.inward.get_by_id(db=db, inward_id=inward_id)
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


@router.post(
    "",
    status_code=200,
    dependencies=[Depends(PermissionChecker(permission="add_inward"))],
)
def add_inward(*, inward_in: InwardCreate, db: Session = Depends(dependencies.get_db)):
    try:
        inward = crud.inward.create(db=db, obj_in=inward_in, items=inward_in.items)
        return inward
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/{inward_id}",
    status_code=200,
    response_model=InwardOnly,
    dependencies=[Depends(PermissionChecker(permission="update_inward"))],
)
def update_inward(
    inward_id: int, inward_in: InwardUpdate, db: Session = Depends(dependencies.get_db)
):
    try:
        inward = crud.inward.update(
            db=db, inward_id=inward_id, obj_in=inward_in, items=inward_in.items
        )
        return inward
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{inward_id}",
    status_code=200,
    dependencies=[Depends(PermissionChecker(permission="delete_inward"))],
)
def delete_inward(*, inward_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete inward
    """
    result = crud.inward.get_by_id(db=db, id=inward_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Inward with ID {inward_id} not found",
        )

    result.status = 0
    db.commit()

    return "Inward Deleted successfully"


@router.get("/{supplier_id}/items", status_code=200)
def fetch_items_by_supplier_id(
    *,
    supplier_id: int,
    db: Session = Depends(dependencies.get_db),
):
    items = crud.inward.get_items_by_supplier_id(db=db, supplier_id=supplier_id)
    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No items found for supplier with ID {supplier_id}",
        )
    return {"items": items}
