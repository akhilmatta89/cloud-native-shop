"""
OrderCreate

product_id
quantity
OrderUpdate

status
OrderResponse

everything

"""
from datetime import datetime
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import OrderStatus

class OrderCreate(BaseModel):
    """Schema for creating a new order."""
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class OrderUpdate(BaseModel):
    """Schema for updating an existing order."""
    status: OrderStatus

class OrderResponse(BaseModel):
    """Schema for representing an order response."""
    id: int
    product_id: int
    quantity: int
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)