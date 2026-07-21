from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.main import OrderResponse
from app.database import get_db
from app.schemas import OrderCreate
from app.services import OrderService


router = APIRouter()

@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(order_request: OrderCreate, db: Session = Depends(get_db)):
    return OrderService.create_order(db, order_request)

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return OrderService.get_order_by_id(db, order_id)