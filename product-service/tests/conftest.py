from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate


# ==========================================================
# Database Fixture
# ==========================================================

@pytest.fixture
def mock_db():
    """
    Creates a mocked SQLAlchemy Session.
    Used by repository, service and route tests.
    """
    return MagicMock(spec=Session)


# ==========================================================
# FastAPI Test Client
# ==========================================================

@pytest.fixture
def client(mock_db):
    """
    Returns a FastAPI TestClient with the database dependency overridden.
    """

    app.dependency_overrides[get_db] = lambda: mock_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ==========================================================
# Sample Product Model
# ==========================================================

@pytest.fixture
def sample_product():
    """
    Returns a SQLAlchemy Product model instance.
    """

    return Product(
        id=1,
        name="Mechanical Keyboard",
        description="RGB Mechanical Keyboard",
        price=Decimal("89.99"),
        stock_quantity=15,
        is_active=True,
    )


# ==========================================================
# Multiple Products
# ==========================================================

@pytest.fixture
def sample_products():
    """
    Returns a list of Product model instances.
    """

    return [
        Product(
            id=1,
            name="Mechanical Keyboard",
            description="RGB Keyboard",
            price=Decimal("89.99"),
            stock_quantity=15,
            is_active=True,
        ),
        Product(
            id=2,
            name="Gaming Mouse",
            description="Wireless Mouse",
            price=Decimal("49.99"),
            stock_quantity=30,
            is_active=True,
        ),
    ]


# ==========================================================
# ProductCreate Schema
# ==========================================================

@pytest.fixture
def product_create():
    """
    Valid ProductCreate schema.
    """

    return ProductCreate(
        name="Mechanical Keyboard",
        description="RGB Mechanical Keyboard",
        price=Decimal("89.99"),
        stock_quantity=15,
    )


# ==========================================================
# ProductUpdate Schema
# ==========================================================

@pytest.fixture
def product_update():
    """
    Valid ProductUpdate schema.
    """

    return ProductUpdate(
        name="Mechanical Keyboard Pro",
        price=Decimal("99.99"),
    )


# ==========================================================
# Invalid Product Payload
# ==========================================================

@pytest.fixture
def invalid_product_payload():
    """
    Invalid payload used for validation tests.
    """

    return {
        "name": "",
        "description": "Invalid Product",
        "price": -10,
        "stock_quantity": -5,
    }


# ==========================================================
# Valid JSON Payload
# ==========================================================

@pytest.fixture
def valid_payload():
    """
    JSON payload used by API route tests.
    """

    return {
        "name": "Mechanical Keyboard",
        "description": "RGB Mechanical Keyboard",
        "price": "89.99",
        "stock_quantity": 15,
    }


# ==========================================================
# Updated JSON Payload
# ==========================================================

@pytest.fixture
def update_payload():
    """
    JSON payload for update requests.
    """

    return {
        "name": "Mechanical Keyboard Pro",
        "price": "99.99",
    }