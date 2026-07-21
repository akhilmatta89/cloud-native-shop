from sqlalchemy.orm import Session

from app.models import Order
from app.models import OrderStatus

class OrderRepository:

    @staticmethod
    def create_order(db: Session, order: Order) -> Order:
        """Logic to create a new order in the database"""
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order | None:
        """Logic to retrieve an order from the database"""
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_all_orders(db: Session) -> list[Order]:
        """Logic to retrieve all orders from the database"""
        return db.query(Order).all()

    @staticmethod
    def update_order_status(db: Session, order_id: int, status: OrderStatus) -> Order | None:
        """Logic to update the status of an existing order in the database"""
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            db.commit()
            db.refresh(order)
        return order

    @staticmethod
    def delete_order(db: Session, order_id: int) -> Order | None:
        """Logic to delete an order from the database"""
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            db.delete(order)
            db.commit()
        return order