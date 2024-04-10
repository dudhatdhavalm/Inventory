from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
)
from db.base_class import Base


class ContactDetail(Base):
    id = Column(Integer, primary_key=True)
    contact_name = Column(String)
    mobile_number = Column(String)
    phone_number = Column(String)
    email = Column(String)
    pan_no = Column(String)
    gstin = Column(String)

    supplier_id = Column(
        Integer,
        ForeignKey("supplier.id"),
        nullable=True,
    )
