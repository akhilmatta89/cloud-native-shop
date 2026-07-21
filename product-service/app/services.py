from sqlalchemy.orm import Session

from app.models import Product
from app.repositories import ProductRepository
from app.schemas import ProductCreate, ProductUpdate
from app.exceptions import ProductNotFoundException
from app.logger import logger


class ProductService:

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        logger.info("Creating a new product")
        product = ProductRepository.create_product(db, product)
        logger.info(
            "Product created successfully. Product ID: %s",
            product.id,
        )

        return product

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product:
        logger.info("Fetching product with ID: %s", product_id)
        product = ProductRepository.get_product_by_id(db, product_id)

        if product is None:
            logger.warning("Product not found. Product ID: %s", product_id)
            raise ProductNotFoundException(product_id)

        logger.info("Product fetched successfully. Product ID: %s", product_id)
        return product

    @staticmethod
    def get_all_products(db: Session) -> list[Product]:
        logger.info("Fetching all products")
        products = ProductRepository.get_all_products(db)
        logger.info("All products fetched successfully. Total products: %s", len(products))
        return products

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_update: ProductUpdate,
    ) -> Product:
        logger.info("Updating product with ID: %s", product_id)
        product = ProductRepository.get_product_by_id(db, product_id)

        if product is None:
            logger.warning("Product not found. Product ID: %s", product_id)
            raise ProductNotFoundException(product_id)

        updated_product = ProductRepository.update_product(
            db,
            product,
            product_update,
        )
        logger.info("Product updated successfully. Product ID: %s", product_id)
        return updated_product

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
    ) -> Product:
        logger.info("Deleting product with ID: %s", product_id)
        product = ProductRepository.get_product_by_id(db, product_id)

        if product is None:
            logger.warning("Product not found. Product ID: %s", product_id)
            raise ProductNotFoundException(product_id)

        deleted_product = ProductRepository.delete_product(
            db,
            product,
        )
        logger.info("Product deleted successfully. Product ID: %s", product_id)
        return deleted_product