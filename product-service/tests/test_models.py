from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Product


# ==========================================================
# SQLite Test Database
# ==========================================================

@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh in-memory SQLite database for every test.
    """

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# ==========================================================
# Product Initialization
# ==========================================================

def test_product_initialization():

    product = Product(
        name="Mechanical Keyboard",
        description="RGB Mechanical Keyboard",
        price=Decimal("89.99"),
        stock_quantity=15,
    )

    assert product.name == "Mechanical Keyboard"
    assert product.description == "RGB Mechanical Keyboard"
    assert product.price == Decimal("89.99")
    assert product.stock_quantity == 15


# ==========================================================
# Database Defaults
# ==========================================================

def test_product_database_defaults(db_session):

    product = Product(
        name="Gaming Mouse",
        description="Wireless Gaming Mouse",
        price=Decimal("49.99"),
        stock_quantity=20,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    assert product.id is not None
    assert product.is_active is True
    assert product.created_at is not None
    assert product.updated_at is not None


# ==========================================================
# Auto Increment
# ==========================================================

def test_product_primary_key_generated(db_session):

    product = Product(
        name="Monitor",
        description="27 Inch Monitor",
        price=Decimal("199.99"),
        stock_quantity=5,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    assert product.id is not None


# ==========================================================
# Multiple Products
# ==========================================================

def test_multiple_products_can_be_saved(db_session):

    product1 = Product(
        name="Keyboard",
        price=Decimal("50.00"),
        stock_quantity=10,
    )

    product2 = Product(
        name="Mouse",
        price=Decimal("25.00"),
        stock_quantity=30,
    )

    db_session.add_all([product1, product2])
    db_session.commit()

    products = db_session.query(Product).all()

    assert len(products) == 2


# ==========================================================
# Soft Delete Flag
# ==========================================================

def test_soft_delete_flag(db_session):

    product = Product(
        name="Laptop",
        price=Decimal("899.99"),
        stock_quantity=5,
    )

    db_session.add(product)
    db_session.commit()

    product.is_active = False

    db_session.commit()
    db_session.refresh(product)

    assert product.is_active is False


# ==========================================================
# Update Timestamp
# ==========================================================

def test_updated_at_changes_after_update(db_session):

    product = Product(
        name="Laptop Stand",
        price=Decimal("29.99"),
        stock_quantity=15,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    original_updated_at = product.updated_at

    product.stock_quantity = 50

    db_session.commit()
    db_session.refresh(product)

    assert product.updated_at >= original_updated_at


# ==========================================================
# Decimal Precision
# ==========================================================

def test_price_is_decimal(db_session):

    product = Product(
        name="SSD",
        price=Decimal("129.99"),
        stock_quantity=12,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    assert isinstance(product.price, Decimal)


# ==========================================================
# Nullable Description
# ==========================================================

def test_description_can_be_none(db_session):

    product = Product(
        name="USB Cable",
        description=None,
        price=Decimal("9.99"),
        stock_quantity=100,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    assert product.description is None


# ==========================================================
# __repr__
# ==========================================================

def test_product_repr():

    product = Product(
        id=1,
        name="Mechanical Keyboard",
    )

    assert repr(product) == "<Product(id=1, name='Mechanical Keyboard')>"


# ==========================================================
# Query Product
# ==========================================================

def test_query_product(db_session):

    product = Product(
        name="Gaming Chair",
        price=Decimal("299.99"),
        stock_quantity=8,
    )

    db_session.add(product)
    db_session.commit()

    saved_product = (
        db_session.query(Product)
        .filter(Product.name == "Gaming Chair")
        .first()
    )

    assert saved_product is not None
    assert saved_product.name == "Gaming Chair"


# ==========================================================
# Update Product
# ==========================================================

def test_update_product(db_session):

    product = Product(
        name="Headphones",
        price=Decimal("99.99"),
        stock_quantity=10,
    )

    db_session.add(product)
    db_session.commit()

    product.price = Decimal("79.99")

    db_session.commit()
    db_session.refresh(product)

    assert product.price == Decimal("79.99")


# ==========================================================
# Delete Product
# ==========================================================

def test_delete_product(db_session):

    product = Product(
        name="Webcam",
        price=Decimal("59.99"),
        stock_quantity=15,
    )

    db_session.add(product)
    db_session.commit()

    db_session.delete(product)
    db_session.commit()

    deleted = (
        db_session.query(Product)
        .filter(Product.name == "Webcam")
        .first()
    )

    assert deleted is None