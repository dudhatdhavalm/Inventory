from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from models.user import User
from schemas.supplier import (
    SupplierBankContactSchema,
    SupplierCreate,
    SupplierOnly,
    SupplierUpdate,
)
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user

router = APIRouter()


@router.get("", status_code=200)
def fetch_all_supplier(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all supplier
    """
    supplier = crud.supplier.get(db=db)
    return supplier


@router.get("/{supplier_id}", status_code=200, response_model=SupplierBankContactSchema)
def fetch_supplier_id(
    *,
    supplier_id: int,
    db: Session = Depends(dependencies.get_db),
) -> SupplierBankContactSchema:
    """
    Fetch supplier by id
    """
    supplier = crud.supplier.get_by_bank_contact_id(db=db, id=supplier_id)

    if not supplier:
        raise HTTPException(
            status_code=404, detail=f"Supplier with ID {supplier_id} not found"
        )

    return supplier


# @router.get("/{supplier_id}", status_code=200)
# def fetch_supplier_bank_contact(
#     *,
#     supplier_id: int,
#     db: Session = Depends(dependencies.get_db),
# ):
#     """
#     Fetch supplier by id
#     """
#     supplier = crud.supplier.get_by_id(db=db, id=supplier_id)
#     if not supplier:
#         raise HTTPException(
#             status_code=404, detail=f"Supplier with ID {supplier_id} not found"
#         )
#     return supplier


@router.post("", status_code=200)
def add_supplier(
    *, supplier_in: SupplierCreate, db: Session = Depends(dependencies.get_db)
):
    try:
        supplier = crud.supplier.create(db=db, obj_in=supplier_in)
        return supplier

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create supplier: {str(e)}"
        )


@router.put("/{supplier_id}", status_code=200, response_model=SupplierOnly)
def update_supplier(
    *,
    request: Request,
    supplier_id: int,
    supplier_in: SupplierUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update Supplier
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    supplier_record = crud.bank_detail.get_by_id(db=db, id=supplier_id)
    supplier_record_id = crud.bank_detail.get_by_id(db=db, id=supplier_in.id)

    if not supplier_record:
        raise HTTPException(
            status_code=404, detail=f"Supplier Detail not found with this id"
        )

    if not supplier_record_id:
        raise HTTPException(
            status_code=404, detail=f"Supplier Detail not found with this id"
        )

    result = crud.supplier.get_by_id(db=db, id=supplier_id)
    supplier = crud.supplier.update(
        db=db, db_obj=result, obj_in=supplier_in, modified_by=modified_by
    )

    return supplier


@router.delete("/{supplier_id}", status_code=200)
def delete_supplier(
    *, supplier_id: int, db: Session = Depends(dependencies.get_db)
) -> dict:
    """
    Delete Supplier
    """
    result = crud.supplier.get_by_id(db=db, id=supplier_id)
    result.status = 0
    db.commit()

    return "Supplier Deleted successfully"
