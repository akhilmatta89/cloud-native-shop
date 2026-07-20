"""
Task: CNS_2.1

Pydantic Schemas for Product Service

- ProductCreate
- ProductUpdate
- ProductResponse
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock_quantity: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    stock_quantity: int | None = None
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: Decimal
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)