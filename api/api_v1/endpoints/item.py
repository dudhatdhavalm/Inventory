from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from models.user import User
from schemas.item import (
    ItemCreate,
    ItemOnly,
    ItemUpdate
)
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user

router = APIRouter()

@router.get("", status_code=200)
def fetch_all_item(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all item
    """
    item = crud.item.get(db=db)
    return item


@router.get("/{item_id}", status_code=200)
def fetch_item_id(
    *,
    item_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch item by id
    """
    item = crud.item.get_by_id(db=db, id=item_id)

    if not item:
        raise HTTPException(
            status_code=404, detail=f"Item with ID {item_id} not found"
        )

    return item


@router.post("", status_code=200)
def add_item(
    *, item_in: ItemCreate, db: Session = Depends(dependencies.get_db)
):
    try:
        item = crud.item.create(db=db, obj_in=item_in)
        return item

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create item: {str(e)}"
        )


@router.put("/{item_id}", status_code=200, response_model=ItemOnly)
def update_item(
    *,
    request: Request,
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update Item
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    result = crud.item.get_by_id(db=db, id=item_in.id)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Item Detail not found with this id"
        )

    res = crud.item.update(
        db=db, db_obj=result, obj_in=item_in, modified_by=modified_by
    )

    return res


@router.delete("/{item_id}", status_code=200)
def delete_item(
    *, item_id: int, db: Session = Depends(dependencies.get_db)
) -> dict:
    """
    Delete Item
    """
    result = crud.item.get_by_id(db=db, id=item_id)
    result.status = 0
    db.commit()

    return "Item Deleted successfully"
