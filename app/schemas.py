from datetime import datetime

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    item_name: str = Field(..., min_length=1, examples=["Burger"])
    quantity: int = Field(..., gt=0, examples=[2])
    price: float = Field(..., gt=0, examples=[9.99])


class OrderResponse(BaseModel):
    id: str
    item_name: str
    quantity: int
    price: float
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
