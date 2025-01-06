from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from db.base_class import Base

class InwardReturn(Base):
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    inward_id = Column(Integer, ForeignKey("inward.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    return_date = Column(DateTime,nullable=False)
    return_reason = Column(String,nullable=False)