from typing import List, Optional
from pydantic import BaseModel


class RolePermissionBase(BaseModel):
    permission_id: int
    roles_id: int

class PermissionModule(BaseModel):
    permission_id: Optional[int]
    
class RolePermissionIn(BaseModel):
    Permission: List[PermissionModule]

class PermissionInDBBase(RolePermissionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class RolePermission(PermissionInDBBase):
    ...