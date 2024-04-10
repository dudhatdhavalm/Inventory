from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
)
from db.base_class import Base


class BankDetail(Base):
    id = Column(Integer, primary_key=True)
    account_no = Column(String)
    branch = Column(String)
    IFSC_code = Column(String)
    bank = Column(String)

    supplier_id = Column(
        Integer,
        ForeignKey("supplier.id"),
        nullable=True,
    )
