from pydantic import BaseModel


class StockDetailsBase(BaseModel):
    item_id: int


class StockDetailsCreate(StockDetailsBase):
    pass
