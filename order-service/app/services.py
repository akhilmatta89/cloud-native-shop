from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Order, OrderStatus
from app.repositories import OrderRepository
from app.schemas import OrderCreate
from app.clients.product_client import ProductClient

class OrderService:
    @staticmethod
    def create_order(db: Session, order_request: OrderCreate) -> Order:
        """
        Business logic to create a new order.
        """

        # Step 1: Fetch product details from Product Service
        product_info = ProductClient.get_product(order_request.product_id)

        # Step 2: Validate product and requested quantity
        OrderService._validate_product(product_info, order_request.quantity)

        # Step 3: Calculate total price
        total_price = OrderService._calculate_total_price(product_info, order_request.quantity)

        # Step 4: Reduce inventory in Product Service
        ProductClient.reduce_inventory(
            order_request.product_id,
            product_info["stock_quantity"] - order_request.quantity,
        )

        # Step 5: Create ORM object
        order = Order(
            product_id=order_request.product_id,
            quantity=order_request.quantity,
            total_price=total_price,
            status=OrderStatus.PENDING,
        )

        # Step 6: Persist order
        return OrderRepository.create_order(db, order)

    @staticmethod
    def _validate_product(product_info: dict, quantity: int):
        """
        Validate product existence, status, and stock.
        """
        if not product_info:
            raise ValueError("Product not found.")

        if not product_info["is_active"]:
            raise ValueError("Product is not active.")

        if product_info["stock_quantity"] < quantity:
            raise ValueError("Insufficient stock for the requested quantity.")

    @staticmethod
    def _calculate_total_price(product_info: dict, quantity: int) -> Decimal:
        """
        Calculate total order price.
        """
        price = Decimal(str(product_info["price"]))

        return price * quantity

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order:
        """
        Retrieve an order by its ID.
        """
        order = OrderRepository.get_order_by_id(db, order_id)
        if not order:
            raise ValueError("Order not found.")
        return order

    @staticmethod
    def get_all_orders(db: Session) -> list[Order]:
        """
        Retrieve all orders.
        """
        return OrderRepository.get_all_orders(db)

    @staticmethod
    def update_order_status(db: Session, order_id: int, status: OrderStatus) -> Order:
        """
        Update the status of an existing order.
        """
        order = OrderRepository.get_order_by_id(db, order_id)

        if not order:
            raise ValueError("Order not found.")

        return OrderRepository.update_order_status(db, order_id, status)

    @staticmethod
    def delete_order(db: Session, order_id: int) -> Order:
        """
        Delete an order by its ID.
        """
        order = OrderRepository.get_order_by_id(db, order_id)

        if not order:
            raise ValueError("Order not found.")

        return OrderRepository.delete_order(db, order_id)