from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from core.permission_checker import PermissionChecker
from models.user import User
from schemas.user import UserDetails, UserOnly, UserCreate, UserInDBBase, UserRoleAssignment, UserUpdate , User as UserRole
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user

router = APIRouter()


# @router.get("/list", status_code=200, response_model=AllUserWithDoc)
# def fetch_all_users(
#     *,
#     db: Session = Depends(dependencies.get_db),
# ) -> AllUserWithDoc:
#     """
#     Fetch all users list
#     """
#     users = crud.user.get_all_user(db=db)
#     res = AllUserWithDoc(items=users)
#     return res


@router.get("", status_code=200,dependencies=[
    Depends(PermissionChecker(permission="read_user"))
])
def fetch_all_users(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all users
    """
    users = crud.user.get_all_user(db=db)
    return users


@router.get("/{user_id}", status_code=200,dependencies=[
    Depends(PermissionChecker(permission="read_user"))
])
def fetch_all_users(
    *,
    user_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch users by id
    """
    user = crud.user.get_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return user


# @router.post("", status_code=200)
# def add_user(
#     *,
#     request: Request,
#     user_in: UserCreate,
#     db: Session = Depends(dependencies.get_db)
# ) -> dict:
#     current_user: User = get_current_user(request)
#     is_super_admin = current_user.is_super_admin

#     if not is_super_admin:
#         raise HTTPException(status_code=404, detail=f"You can not add user")

#     user = crud.user.create(db=db, obj_in=user_in)
#     return user


@router.put("/{user_id}", status_code=200, response_model=UserOnly,dependencies=[
    Depends(PermissionChecker(permission="update_user"))
])
def update_user(
    *,
    request: Request,
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(dependencies.get_db),
) -> dict:
    """
    Update User
    """
    current_user: User = get_current_user(request)
    modified_by = current_user.id

    result = crud.user.get(db=db, id=user_id)
    user = crud.user.update(
        db=db, db_obj=result, obj_in=user_in, modified_by=modified_by
    )

    return user

@router.post("/{user_id}/role", status_code=201, response_model=UserRole,dependencies=[
    Depends(PermissionChecker(permission="user_role_add"))
])
def create_user_role(
    *, user_id: int,role_in: UserRoleAssignment, db: Session = Depends(dependencies.get_db)
) -> dict:
    """
    Assign role to user
    """
    user = crud.user.assign_role(db=db, obj_in=role_in, user_id = user_id)

    return user

@router.delete("/{user_id}", status_code=200,dependencies=[
    Depends(PermissionChecker(permission="delete_user"))
])
def delete_user(*, user_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete User
    """
    result = crud.user.get(db=db, id=user_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found",
        )
    result.status = 0
    db.commit()

    return "User Deleted successfully"
