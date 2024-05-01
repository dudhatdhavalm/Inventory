from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from models.user import User
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from schemas.roles import RolesCreate, RolesOnly, RolesUpdate
from util.user_util import get_current_user

router = APIRouter()


@router.get("", status_code=200)
def fetch_all_roles(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all roles
    """
    roles = crud.roles.get(db=db)
    return roles


@router.get("/{role_id}", status_code=200)
def fetch_role_id(
    *,
    role_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch Role by id
    """
    role = crud.roles.get_by_id(db=db, id=role_id)

    if not role:
        raise HTTPException(status_code=404, detail=f"Item with ID {role_id} not found")

    return role


@router.post("", status_code=200)
def add_role(*, roles_in: RolesCreate, db: Session = Depends(dependencies.get_db)):
    try:
        role = crud.roles.create(db=db, obj_in=roles_in)
        return role

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create role: {str(e)}")


@router.put("/{role_id}", status_code=200, response_model=RolesOnly)
def update_role(
    *,
    request: Request,
    role_id: int,
    role_in: RolesUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update Role
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    result = crud.roles.get_by_id(db=db, id=role_in.id)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Role Detail not found with this id"
        )

    res = crud.roles.update(
        db=db, db_obj=result, obj_in=role_in, modified_by=modified_by
    )

    return res


@router.delete("/{role_id}", status_code=200)
def delete_role(*, role_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete Role
    """
    result = crud.roles.get_by_id(db=db, id=role_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Role with id {role_id} not found",
        )
    result.status = 0
    db.commit()

    return "Role Deleted successfully"
