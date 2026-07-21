from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models import Product   # IMPORTANT
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# ==========================================================
# Test Data
# ==========================================================

def create_sample_product():

    payload = {
        "name": "Mechanical Keyboard",
        "description": "RGB Keyboard",
        "price": 89.99,
        "stock_quantity": 10,
    }

    response = client.post(
        "/products",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


# ==========================================================
# POST
# ==========================================================

def test_create_product():

    payload = {
        "name": "Gaming Mouse",
        "description": "Wireless Mouse",
        "price": 49.99,
        "stock_quantity": 20,
    }

    response = client.post(
        "/products",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert float(data["price"]) == payload["price"]
    assert data["stock_quantity"] == payload["stock_quantity"]


# ==========================================================
# GET BY ID
# ==========================================================

def test_get_product():

    product = create_sample_product()

    response = client.get(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product["id"]
    assert data["name"] == product["name"]


# ==========================================================
# GET ALL
# ==========================================================

def test_get_all_products():

    create_sample_product()

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


# ==========================================================
# UPDATE
# ==========================================================

def test_update_product():

    product = create_sample_product()

    update_payload = {
        "name": "Gaming Keyboard",
        "price": 99.99,
        "stock_quantity": 25,
    }

    response = client.put(
        f"/products/{product['id']}",
        json=update_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Gaming Keyboard"
    assert float(data["price"]) == 99.99
    assert data["stock_quantity"] == 25


# ==========================================================
# DELETE
# ==========================================================

def test_delete_product():

    product = create_sample_product()

    response = client.delete(
        f"/products/{product['id']}"
    )

    assert response.status_code == 200

    deleted = response.json()

    assert deleted["is_active"] is False


# ==========================================================
# VERIFY SOFT DELETE
# ==========================================================

def test_deleted_product_not_returned():

    product = create_sample_product()

    client.delete(
        f"/products/{product['id']}"
    )

    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()

    ids = [p["id"] for p in products]

    assert product["id"] not in ids


# ==========================================================
# INVALID CREATE
# ==========================================================

def test_invalid_create_product():

    response = client.post(
        "/products",
        json={
            "name": "",
            "price": -10,
            "stock_quantity": -1,
        },
    )

    assert response.status_code == 422


# ==========================================================
# INVALID PRODUCT ID
# ==========================================================

def test_get_non_existing_product():

    response = client.get("/products/99999")

    assert response.status_code == 404


def test_update_non_existing_product():

    response = client.put(
        "/products/99999",
        json={
            "price": 10,
        },
    )

    assert response.status_code == 404


def test_delete_non_existing_product():

    response = client.delete("/products/99999")

    assert response.status_code == 404


# ==========================================================
# INVALID PATH PARAMETER
# ==========================================================

def test_invalid_path_parameter():

    response = client.get("/products/abc")

    assert response.status_code == 422