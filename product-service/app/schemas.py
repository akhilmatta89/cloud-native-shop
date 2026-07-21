"""
Task: CNS_2.1

Pydantic Schemas for Product Service

- ProductCreate
- ProductUpdate
- ProductResponse
"""

from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

CleanNameString = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=100)
]

class ProductCreate(BaseModel):
    name: CleanNameString
    description: str | None = Field(default=None, max_length=500)
    price: Decimal = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    name: CleanNameString | None = None
    description: str | None = Field(default=None, max_length=500)
    price: Decimal | None = Field(default=None, gt=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)