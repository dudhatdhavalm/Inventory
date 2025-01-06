from pydantic import BaseModel


class OutwardReturnCreate(BaseModel):
    outward_item_id: int
    quantity: int
    return_reason: str


class OutwardReturnResponse(BaseModel):
    message: str
