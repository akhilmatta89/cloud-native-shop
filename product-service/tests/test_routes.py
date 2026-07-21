from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.database import get_db
from app.exceptions import ProductNotFoundException
from app.main import app
from app.models import Product
from app.services import ProductService


# ==========================================================
# Test Client Fixture
# ==========================================================

@pytest.fixture
def client():
    def override_get_db():
        yield MagicMock()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# ==========================================================
# Sample Product
# ==========================================================

@pytest.fixture
def sample_product():
    return Product(
        id=1,
        name="Mechanical Keyboard",
        description="RGB Keyboard",
        price=Decimal("89.99"),
        stock_quantity=10,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def product_payload():
    return {
        "name": "Mechanical Keyboard",
        "description": "RGB Keyboard",
        "price": 89.99,
        "stock_quantity": 10,
    }


@pytest.fixture
def update_payload():
    return {
        "name": "Gaming Keyboard",
        "price": 99.99,
        "stock_quantity": 25,
    }


# ==========================================================
# POST /products
# ==========================================================

def test_create_product(
    client,
    sample_product,
    product_payload,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "create_product",
        lambda db, product: sample_product,
    )

    response = client.post(
        "/products",
        json=product_payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Mechanical Keyboard"


# ==========================================================
# GET /products/{id}
# ==========================================================

def test_get_product(
    client,
    sample_product,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "get_product_by_id",
        lambda db, product_id: sample_product,
    )

    response = client.get("/products/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Mechanical Keyboard"


def test_get_product_not_found(
    client,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "get_product_by_id",
        lambda db, product_id: (_ for _ in ()).throw(
            ProductNotFoundException(product_id)
        ),
    )

    response = client.get("/products/999")

    assert response.status_code == 404


# ==========================================================
# GET /products
# ==========================================================

def test_get_all_products(
    client,
    sample_product,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "get_all_products",
        lambda db: [sample_product],
    )

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == 1


def test_get_all_products_empty(
    client,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "get_all_products",
        lambda db: [],
    )

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == []


# ==========================================================
# PUT /products/{id}
# ==========================================================

def test_update_product(
    client,
    sample_product,
    update_payload,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "update_product",
        lambda db, product_id, product_update: sample_product,
    )

    response = client.put(
        "/products/1",
        json=update_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1


def test_update_product_not_found(
    client,
    update_payload,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "update_product",
        lambda db, product_id, product_update: (_ for _ in ()).throw(
            ProductNotFoundException(product_id)
        ),
    )

    response = client.put(
        "/products/999",
        json=update_payload,
    )

    assert response.status_code == 404


# ==========================================================
# DELETE /products/{id}
# ==========================================================

def test_delete_product(
    client,
    sample_product,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "delete_product",
        lambda db, product_id: sample_product,
    )

    response = client.delete("/products/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1


def test_delete_product_not_found(
    client,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductService,
        "delete_product",
        lambda db, product_id: (_ for _ in ()).throw(
            ProductNotFoundException(product_id)
        ),
    )

    response = client.delete("/products/999")

    assert response.status_code == 404


# ==========================================================
# Validation Tests
# ==========================================================

def test_create_product_validation(client):

    response = client.post(
        "/products",
        json={
            "name": "",
            "price": -10,
            "stock_quantity": -5,
        },
    )

    assert response.status_code == 422


def test_update_product_validation(client):

    response = client.put(
        "/products/1",
        json={
            "price": -100,
        },
    )

    assert response.status_code == 422


def test_invalid_product_id(client):

    response = client.get("/products/abc")

    assert response.status_code == 422