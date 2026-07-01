from sqlalchemy.sql import func

from .database import Base
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text(), nullable=True)
    price = Column(Numeric(10,2), nullable=False)
    stock_quantity = Column(Integer(), nullable=False)
    is_active = Column(Boolean(),nullable=False, default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}')>"