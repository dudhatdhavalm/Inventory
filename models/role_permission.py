from sqlalchemy import Column, ForeignKey, Integer
from db.base_class import Base


class RolePermission(Base):
    id = Column(Integer, primary_key=True)
    permission_id = Column(
        Integer,
        ForeignKey('permission.id'),nullable=True,
    )
    roles_id= Column(
        Integer,
        ForeignKey('roles.id'),nullable=True,
    )