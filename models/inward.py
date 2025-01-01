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
    invoice_no = Column(String)
    challan_no = Column(String)
    gst_no = Column(String)
    supplier_id = Column(
        Integer,
        ForeignKey("supplier.id"),
        nullable=True,
    )
    supplier_name = Column(String,nullable=True)
    grand_total = Column(Integer)

class InwardItem(Base):
    id = Column(Integer,primary_key=True)
    item_id = Column(Integer,ForeignKey("item.id"),nullable=False)
    inward_id = Column(Integer,ForeignKey("inward.id"),nullable=False)
    name = Column(String,nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
    total_price = Column(Integer)