from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from models.user import User
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from schemas.permission import PermissionCreate, PermissionOnly, PermissionUpdate
from schemas.role_permission import RolePermissionIn , RolePermission
from util.user_util import get_current_user

router = APIRouter()


@router.get("", status_code=200)
def fetch_all_permission(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all permission
    """
    permission = crud.permission.get(db=db)
    return permission


@router.get("/{permission_id}", status_code=200)
def fetch_permission_id(
    *,
    permission_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch permission by id
    """
    permission = crud.permission.get_by_id(db=db, id=permission_id)

    if not permission:
        raise HTTPException(status_code=404, detail=f"Item with ID {permission_id} not found")

    return permission


@router.post("", status_code=200)
def add_permission(*, permission_in: PermissionCreate, db: Session = Depends(dependencies.get_db)):
    try:
        permission = crud.permission.create(db=db, obj_in=permission_in)
        return permission

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create item: {str(e)}")


@router.put("/{permission_id}", status_code=200, response_model=PermissionOnly)
def update_item(
    *,
    request: Request,
    permission_id: int,
    permission_in: PermissionUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update Permission
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    result = crud.permission.get_by_id(db=db, id=permission_in.id)

    if not result:
        raise HTTPException(
            status_code=404, detail=f"Permission Detail not found with this id"
        )

    res = crud.permission.update(
        db=db, db_obj=result, obj_in=permission_in, modified_by=modified_by
    )

    return res

@router.post("/{role_id}/role", status_code=201, response_model=List[RolePermission])
def assign_permission(
    *, role_id: int,permission_in: RolePermissionIn, db: Session = Depends(dependencies.get_db)
) -> dict:
    """
    Assign permission to role
    """
    roles = crud.role_permission.assign_permission(db=db, obj_in=permission_in, role_id = role_id)
    return roles


@router.delete("/{permission_id}", status_code=200)
def delete_permission(*, permission_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete Permission
    """
    result = crud.permission.get_by_id(db=db, id=permission_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Permission with id {permission_id} not found",
        )
    result.status = 0
    db.commit()

    return "Permission Deleted successfully"
