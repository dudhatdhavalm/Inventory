from sqlalchemy import (
    Column,
    Integer,
    String,
)
from db.base_class import Base


class Supplier(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    pincode = Column(String)
    distance = Column(String)
    station = Column(String)
    transport = Column(String)
