from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from db.base_class import Base

class StockDetails(Base):
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    available_quantity = Column(Integer, nullable=False)