from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from core.permission_checker import PermissionChecker
from models.user import User
from schemas.item import ItemCreate, ItemOnly, ItemSearch, ItemSearchResults, ItemUpdate
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user

router = APIRouter()


@router.get("", status_code=200,dependencies=[
    Depends(PermissionChecker(permission="read_item"))
])
def fetch_all_item(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all item
    """
    item = crud.item.get(db=db)
    return item


@router.get("/{item_id}", status_code=200,dependencies=[
    Depends(PermissionChecker(permission="read_item"))
])
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
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")

    return item


@router.post("", status_code=200,dependencies=[
    Depends(PermissionChecker(permission="read_item"))
])
def add_item(*, item_in: ItemCreate, db: Session = Depends(dependencies.get_db)):
    try:
        item = crud.item.create(db=db, obj_in=item_in)
        return item

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create item: {str(e)}")


@router.post("/search", status_code=200)
def search_item(
    *,
    name: str = None,
    db: Session = Depends(dependencies.get_db),
):
    """
    Search for item based on label keyword
    """

    item = crud.item.get(db=db, name=name)
    return item


@router.put("/{item_id}", status_code=200, response_model=ItemOnly,dependencies=[
    Depends(PermissionChecker(permission="read_item"))
])
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


@router.delete("/{item_id}", status_code=200,dependencies=[
    Depends(PermissionChecker(permission="read_item"))
])
def delete_item(*, item_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete Item
    """
    result = crud.item.get_by_id(db=db, id=item_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Item with id {item_id} not found",
        )
    result.status = 0
    db.commit()

    return "Item Deleted successfully"
