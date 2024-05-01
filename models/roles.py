from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,DateTime
)
from db.base_class import Base
from sqlalchemy.orm import relationship


class Roles(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(56), nullable=False)
    user = relationship("User",secondary="user_roles",back_populates="roles")
    created_by = Column(
        Integer,
        ForeignKey('user.id'),nullable=True,
    )
    modified_by = Column(
        Integer,
        ForeignKey('user.id'),nullable=True,
    )