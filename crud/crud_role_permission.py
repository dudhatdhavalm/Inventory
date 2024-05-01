from typing import Any
from crud.base import CRUDBase
from sqlalchemy.orm import Session
from models.permission import Permission
from models.role_permission import RolePermission
from schemas.role_permission import RolePermissionIn
from schemas.role_permission import RolePermission as RolePermissionSchema


class CRUDRolePermission(CRUDBase[RolePermission, RolePermissionSchema, None]):
        
    def assign_permission(self, db: Session, obj_in: RolePermissionIn, role_id: int):
        # db.query(RolePermission).filter(RolePermission.roles_id==role_id).delete()
        # db.commit()
        role_permission_obj = []
        for data in obj_in.Permission:
            role_permission_obj.append(RolePermission(roles_id=role_id,permission_id=data.permission_id))
        db.add_all(role_permission_obj)
        db.commit()
        return role_permission_obj
    
    def get_permissions_by_role(self, db:Session, id: Any):
        data = db.query(Permission.name,RolePermission).join(Permission).filter(RolePermission.roles_id==id).all()
        return data
      
    # def get_assigned_permissions(self, db: Session, role_id: int):
    #     permission_obj=db.query(RolePermission).filter(RolePermission.roles_id==role_id).all()      
    #     return permission_obj

role_permission = CRUDRolePermission(RolePermission)
