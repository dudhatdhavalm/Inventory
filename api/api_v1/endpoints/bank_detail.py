from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from models.user import User
from schemas.bank_detail import BankDetailCreate, BankDetailOnly, BankDetailUpdate
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user

router = APIRouter()


@router.get("", status_code=200)
def fetch_all_bank_detail(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all bank detail
    """
    bank_detail = crud.bank_detail.get(db=db)
    return bank_detail


@router.get("/{bank_detail_id}", status_code=200)
def fetch_bank_detail_id(
    *,
    bank_detail_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch bank detail by id
    """
    bank_detail = crud.bank_detail.get_by_id(db=db, id=bank_detail_id)
    if not bank_detail:
        raise HTTPException(
            status_code=404, detail=f"Bank Detail with ID {bank_detail_id} not found"
        )
    return bank_detail

@router.get("/{supplier_id}/supplier", status_code=200)
def fetch_by_supplier_id(
    *,
    supplier_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch contact detail by supplier id
    """
    bank_detail = crud.bank_detail.get_by_supplier_id(db=db, id=supplier_id)
    if not bank_detail:
        raise HTTPException(
            status_code=404,
            detail=f"Supplier with ID {supplier_id} not found",
        )
    return bank_detail

@router.post("", status_code=200)
def add_bank_detail(
    *, bank_detail_in: BankDetailCreate, db: Session = Depends(dependencies.get_db)
):
    bank_detail = crud.bank_detail.create(db=db, obj_in=bank_detail_in)
    return bank_detail


@router.put("/{bank_detail_id}", status_code=200, response_model=BankDetailOnly)
def update_bank_detail(
    *,
    request: Request,
    bank_detail_id: int,
    bank_detail_in: BankDetailUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update Bank Detail
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    bank_detail_record = crud.bank_detail.get_by_id(db=db,id=bank_detail_id)
    bank_detail_record_id = crud.bank_detail.get_by_id(db=db,id=bank_detail_in.id)
 
    if not bank_detail_record:
        raise HTTPException(
            status_code=404, detail=f"Bank Detail not found with this id"
        )
    
    if not bank_detail_record_id:
        raise HTTPException(
            status_code=404, detail=f"Bank Detail not found with this id"
        )

    result = crud.bank_detail.get_by_id(db=db, id=bank_detail_id)
    bank_detail = crud.bank_detail.update(
        db=db, db_obj=result, obj_in=bank_detail_in, modified_by=modified_by
    )

    return bank_detail


@router.delete("/{bank_detail_id}", status_code=200)
def delete_bank_detail(
    *, bank_detail_id: int, db: Session = Depends(dependencies.get_db)
) -> dict:
    """
    Delete Bank Detail
    """
    result = crud.bank_detail.get_by_id(db=db, id=bank_detail_id)
    result.status = 0
    db.commit()

    return "Bank Detail Deleted successfully"
