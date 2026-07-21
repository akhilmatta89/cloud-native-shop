from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.exceptions import ProductNotFoundException
from app.models import Product
from app.repositories import ProductRepository
from app.schemas import ProductCreate, ProductUpdate
from app.services import ProductService


# ==========================================================
# Fixtures
# ==========================================================

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def sample_product():
    return Product(
        id=1,
        name="Mechanical Keyboard",
        description="RGB Keyboard",
        price=Decimal("89.99"),
        stock_quantity=10,
        is_active=True,
    )


@pytest.fixture
def product_create():
    return ProductCreate(
        name="Mechanical Keyboard",
        description="RGB Keyboard",
        price=Decimal("89.99"),
        stock_quantity=10,
    )


@pytest.fixture
def product_update():
    return ProductUpdate(
        name="Gaming Keyboard",
        price=Decimal("99.99"),
        stock_quantity=20,
    )


# ==========================================================
# create_product
# ==========================================================

def test_create_product(
    mock_db,
    product_create,
    sample_product,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "create_product",
        lambda db, product: sample_product,
    )

    product = ProductService.create_product(
        mock_db,
        product_create,
    )

    assert product == sample_product
    assert product.id == 1
    assert product.name == "Mechanical Keyboard"


# ==========================================================
# get_product_by_id
# ==========================================================

def test_get_product_by_id(
    mock_db,
    sample_product,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_product_by_id",
        lambda db, product_id: sample_product,
    )

    product = ProductService.get_product_by_id(
        mock_db,
        1,
    )

    assert product == sample_product


def test_get_product_by_id_not_found(
    mock_db,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_product_by_id",
        lambda db, product_id: None,
    )

    with pytest.raises(ProductNotFoundException):

        ProductService.get_product_by_id(
            mock_db,
            999,
        )


# ==========================================================
# get_all_products
# ==========================================================

def test_get_all_products(
    mock_db,
    sample_product,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_all_products",
        lambda db: [sample_product],
    )

    products = ProductService.get_all_products(mock_db)

    assert len(products) == 1
    assert products[0].id == 1


def test_get_all_products_empty(
    mock_db,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_all_products",
        lambda db: [],
    )

    products = ProductService.get_all_products(mock_db)

    assert products == []


# ==========================================================
# update_product
# ==========================================================

def test_update_product(
    mock_db,
    sample_product,
    product_update,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_product_by_id",
        lambda db, product_id: sample_product,
    )

    monkeypatch.setattr(
        ProductRepository,
        "update_product",
        lambda db, product, update: sample_product,
    )

    product = ProductService.update_product(
        mock_db,
        1,
        product_update,
    )

    assert product == sample_product


def test_update_product_not_found(
    mock_db,
    product_update,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_product_by_id",
        lambda db, product_id: None,
    )

    with pytest.raises(ProductNotFoundException):

        ProductService.update_product(
            mock_db,
            999,
            product_update,
        )


# ==========================================================
# delete_product
# ==========================================================

def test_delete_product(
    mock_db,
    sample_product,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_product_by_id",
        lambda db, product_id: sample_product,
    )

    monkeypatch.setattr(
        ProductRepository,
        "delete_product",
        lambda db, product: sample_product,
    )

    product = ProductService.delete_product(
        mock_db,
        1,
    )

    assert product == sample_product


def test_delete_product_not_found(
    mock_db,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_product_by_id",
        lambda db, product_id: None,
    )

    with pytest.raises(ProductNotFoundException):

        ProductService.delete_product(
            mock_db,
            999,
        )


# ==========================================================
# ProductNotFoundException Message
# ==========================================================

def test_product_not_found_exception_message(
    mock_db,
    monkeypatch,
):

    monkeypatch.setattr(
        ProductRepository,
        "get_product_by_id",
        lambda db, product_id: None,
    )

    with pytest.raises(ProductNotFoundException) as exc:

        ProductService.get_product_by_id(
            mock_db,
            500,
        )

    assert "500" in str(exc.value)