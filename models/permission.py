from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,DateTime
)
from db.base_class import Base


class Permission(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False, unique=True)
    display_name = Column(String(500),nullable= False)
    created_by = Column(
        Integer,
        ForeignKey('user.id'),nullable=True,
    )
    modified_by = Column(
        Integer,
        ForeignKey('user.id'),nullable=True,
    )
