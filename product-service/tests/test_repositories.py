from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from app.models import Product
from app.repositories import ProductRepository
from app.schemas import ProductCreate, ProductUpdate


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
        stock_quantity=25,
    )


# ==========================================================
# create_product
# ==========================================================

def test_create_product(mock_db, product_create):

    product = ProductRepository.create_product(
        mock_db,
        product_create,
    )

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert product.name == product_create.name
    assert product.description == product_create.description
    assert product.price == product_create.price
    assert product.stock_quantity == product_create.stock_quantity


# ==========================================================
# get_product_by_id
# ==========================================================

def test_get_product_by_id_found(mock_db, sample_product):

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = sample_product

    product = ProductRepository.get_product_by_id(
        mock_db,
        1,
    )

    assert product == sample_product

    mock_db.query.assert_called_once_with(Product)
    mock_query.filter.assert_called_once()
    mock_filter.first.assert_called_once()


def test_get_product_by_id_not_found(mock_db):

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.first.return_value = None

    product = ProductRepository.get_product_by_id(
        mock_db,
        999,
    )

    assert product is None


# ==========================================================
# get_all_products
# ==========================================================

def test_get_all_products(mock_db, sample_product):

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = [sample_product]

    products = ProductRepository.get_all_products(mock_db)

    assert len(products) == 1
    assert products[0].name == "Mechanical Keyboard"

    mock_db.query.assert_called_once_with(Product)
    mock_query.filter.assert_called_once()
    mock_filter.all.assert_called_once()


def test_get_all_products_empty(mock_db):

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.all.return_value = []

    products = ProductRepository.get_all_products(mock_db)

    assert products == []


# ==========================================================
# update_product
# ==========================================================

def test_update_product(
    mock_db,
    sample_product,
    product_update,
):

    updated_product = ProductRepository.update_product(
        mock_db,
        sample_product,
        product_update,
    )

    assert updated_product.name == "Gaming Keyboard"
    assert updated_product.price == Decimal("99.99")
    assert updated_product.stock_quantity == 25

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sample_product)


def test_partial_update_product(
    mock_db,
    sample_product,
):

    update = ProductUpdate(
        stock_quantity=100,
    )

    updated_product = ProductRepository.update_product(
        mock_db,
        sample_product,
        update,
    )

    assert updated_product.name == "Mechanical Keyboard"
    assert updated_product.stock_quantity == 100

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


# ==========================================================
# delete_product
# ==========================================================

def test_delete_product(
    mock_db,
    sample_product,
):

    deleted_product = ProductRepository.delete_product(
        mock_db,
        sample_product,
    )

    assert deleted_product.is_active is False

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sample_product)


def test_delete_product_already_inactive(
    mock_db,
    sample_product,
):

    sample_product.is_active = False

    deleted_product = ProductRepository.delete_product(
        mock_db,
        sample_product,
    )

    assert deleted_product.is_active is False

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sample_product)