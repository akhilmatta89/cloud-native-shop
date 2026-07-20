"""CNS_2.2 -> Create a repository layer for the Product Service to handle database operations."""

from sqlalchemy.orm import Session
from app.schemas import ProductCreate, ProductUpdate
from app.models import Product


class ProductRepository:
    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Product | None:
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_all_products(db: Session) -> list[Product]:
        return db.query(Product).filter(Product.is_active == True).all()

    @staticmethod
    def update_product(
            db: Session,
            product: Product,
            product_update: ProductUpdate,
            ) -> Product:
        update_data = product_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete_product(db: Session, product: Product) -> Product:
        product.is_active = False
        db.commit()
        db.refresh(product)
        return product