""" Task:CNS_2.3
Create service module for managing products. """

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Product
from app.repositories import ProductRepository
from app.schemas import ProductCreate, ProductUpdate


class ProductService:

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        return ProductRepository.create_product(db, product)

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        product = ProductRepository.get_product_by_id(db, product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product

    @staticmethod
    def get_all_products(db: Session) -> list[Product]:
        return ProductRepository.get_all_products(db)

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_update: ProductUpdate,
    ) -> Product:

        product = ProductRepository.get_product_by_id(db, product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return ProductRepository.update_product(
            db,
            product,
            product_update,
        )

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
    ) -> Product:

        product = ProductRepository.get_product_by_id(db, product_id)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return ProductRepository.delete_product(
            db,
            product,
        )