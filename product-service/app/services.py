""" Task:CNS_2.3
Create service module for managing products. """

from sqlalchemy.orm import Session

from app.models import Product
from app.repositories import ProductRepository
from app.schemas import ProductCreate, ProductUpdate


class ProductService:

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        return ProductRepository.create_product(db, product)

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product | None:
        return ProductRepository.get_product_by_id(db, product_id)

    @staticmethod
    def get_all_products(db: Session) -> list[Product]:
        return ProductRepository.get_all_products(db)

    @staticmethod
    def update_product(
        db: Session,
        product: Product,
        product_update: ProductUpdate,
    ) -> Product:
        return ProductRepository.update_product(db, product, product_update)

    @staticmethod
    def delete_product(db: Session, product: Product) -> Product:
        return ProductRepository.delete_product(db, product)