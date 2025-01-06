from pydantic import BaseModel


class InwardReturnCreate(BaseModel):
    inward_item_id: int
    quantity: int
    return_reason: str


class InwardReturnResponse(BaseModel):
    message: str
