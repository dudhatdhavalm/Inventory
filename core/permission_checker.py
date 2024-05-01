from enum import Enum
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from api import dependencies
import crud
from schemas.user import User

class PermissionChecker:
    def __init__(self, permission: str):
        self.permission = permission.lower()

    def __call__(self, request: Request, db: Session = Depends(dependencies.get_db)):
        current_user: User = dependencies.get_current_user(request)
        if current_user.is_super_admin:
            return
        
        user_data:User=crud.user.get(db=db,id=current_user.id)
        
        user_permissions = set()
        for role in user_data.roles:
            role_permissions = crud.role_permission.get_permissions_by_role(db=db,id=role.id)
            for permission in role_permissions:
                user_permissions.add(permission.name.lower())

        print(self.permission)
        print(user_permissions)
        if self.permission in user_permissions:
            return True
        
        else:
            raise HTTPException(status_code=403, detail="You don't have permission to access this resource.")