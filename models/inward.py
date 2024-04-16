from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,DateTime
)
from db.base_class import Base


class Inward(Base):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), nullable=False)
    rate = Column(Integer)
    invoice_no = Column(String)
    quantity = Column(Integer)
    grand_total = Column(Integer)
    challan_no = Column(String)
    gst_no = Column(String)
    type = Column(String)
    supplier_id = Column(
        Integer,
        ForeignKey("supplier.id"),
        nullable=True,
    )
    item_id = Column(
        Integer,
        ForeignKey("item.id"),
        nullable=True,
    )