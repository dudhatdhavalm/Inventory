from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from db.base_class import Base


class Outward(Base):
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
    grand_total = Column(Integer)


class OutwardItem(Base):
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    outward_id = Column(Integer, ForeignKey("outward.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
    total_price = Column(Integer)
