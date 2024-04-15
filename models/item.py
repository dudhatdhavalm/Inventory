from sqlalchemy import (
    Column,
    Integer,
    String,
)
from db.base_class import Base


class Item(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    gst = Column(String, nullable=False)
    rate = Column(Integer)
    unit = Column(String, nullable=False)
    cost_rate = Column(Integer)
    final_rate = Column(Integer)
