from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from models.user import User
from schemas.contact_detail import (
    ContactDetailCreate,
    ContactDetailOnly,
    ContactDetailUpdate,
)
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user

router = APIRouter()


@router.get("", status_code=200)
def fetch_all_contact_detail(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all contact detail
    """
    contact_detail = crud.contact_detail.get(db=db)
    return contact_detail


@router.get("/{contact_detail_id}", status_code=200)
def fetch_contact_detail_id(
    *,
    contact_detail_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch contact detail by id
    """
    contact_detail = crud.contact_detail.get_by_id(db=db, id=contact_detail_id)
    if not contact_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Contact Detail with ID {contact_detail_id} not found",
        )
    return contact_detail

@router.get("/{supplier_id}/supplier", status_code=200)
def fetch_by_supplier_id(
    *,
    supplier_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch contact detail by supplier id
    """
    contact_detail = crud.contact_detail.get_by_supplier_id(db=db, id=supplier_id)
    if not contact_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Supplier with ID {supplier_id} not found",
        )
    return contact_detail


@router.post("", status_code=200)
def add_contact_detail(
    *,
    contact_detail_in: ContactDetailCreate,
    db: Session = Depends(dependencies.get_db),
) :
    contact_detail = crud.contact_detail.create(db=db, obj_in=contact_detail_in)
    return contact_detail


@router.put("/{contact_detail_id}", status_code=200, response_model=ContactDetailOnly)
def update_contact_detail(
    *,
    request: Request,
    contact_detail_id: int,
    contact_detail_in: ContactDetailUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update Contact Detail
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    contact_detail_record_id = crud.contact_detail.get_by_id(db=db,id=contact_detail_in.id)
     
    if not contact_detail_record_id:
        raise HTTPException(
            status_code=404, detail=f"Contact Detail not found with this id"
        )

    result = crud.contact_detail.get_by_id(db=db, id=contact_detail_id)
    contact_detail = crud.contact_detail.update(
        db=db, db_obj=result, obj_in=contact_detail_in, modified_by=modified_by
    )

    return contact_detail


@router.delete("/{contact_detail_id}", status_code=200)
def delete_contact_detail(
    *, contact_detail_id: int, db: Session = Depends(dependencies.get_db)
) -> dict:
    """
    Delete Contact Detail
    """
    result = crud.contact_detail.get_by_id(db=db, id=contact_detail_id)
    result.status = 0
    db.commit()

    return "Contact Detail Deleted successfully"
