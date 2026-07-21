from decimal import Decimal
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas import ProductCreate, ProductUpdate, ProductResponse


# ==========================================================
# ProductCreate Tests
# ==========================================================

def test_product_create_valid(product_create):
    """Verify a valid ProductCreate schema."""

    assert product_create.name == "Mechanical Keyboard"
    assert product_create.price == Decimal("89.99")
    assert product_create.stock_quantity == 15


def test_product_create_string_conversion():
    """Pydantic should convert compatible strings."""

    product = ProductCreate(
        name="Gaming Mouse",
        description="Wireless Gaming Mouse",
        price="49.99",
        stock_quantity="20",
    )

    assert product.price == Decimal("49.99")
    assert product.stock_quantity == 20


def test_product_create_missing_name():

    with pytest.raises(ValidationError):

        ProductCreate(
            description="Test",
            price=10,
            stock_quantity=1,
        )


def test_product_create_empty_name():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="",
            description="Test",
            price=10,
            stock_quantity=1,
        )


def test_product_create_name_too_short():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="AB",
            description="Test",
            price=10,
            stock_quantity=1,
        )


def test_product_create_name_too_long():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="A" * 101,
            description="Test",
            price=10,
            stock_quantity=1,
        )


def test_product_create_negative_price():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="Keyboard",
            description="Test",
            price=-10,
            stock_quantity=1,
        )


def test_product_create_zero_price():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="Keyboard",
            description="Test",
            price=0,
            stock_quantity=1,
        )


def test_product_create_negative_stock():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="Keyboard",
            description="Test",
            price=10,
            stock_quantity=-1,
        )


def test_product_create_invalid_price():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="Keyboard",
            description="Test",
            price="abc",
            stock_quantity=1,
        )


def test_product_create_invalid_stock():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="Keyboard",
            description="Test",
            price=10,
            stock_quantity="xyz",
        )


def test_product_create_long_description():

    with pytest.raises(ValidationError):

        ProductCreate(
            name="Keyboard",
            description="A" * 501,
            price=10,
            stock_quantity=1,
        )


def test_product_create_strip_whitespace():

    product = ProductCreate(
        name="     Mechanical Keyboard      ",
        description="RGB",
        price=20,
        stock_quantity=5,
    )

    assert product.name == "Mechanical Keyboard"


def test_product_create_empty_description_allowed():

    product = ProductCreate(
        name="Keyboard",
        description="",
        price=10,
        stock_quantity=1,
    )

    assert product.description == ""


# ==========================================================
# ProductUpdate Tests
# ==========================================================

def test_product_update_partial():

    update = ProductUpdate(
        stock_quantity=25,
    )

    assert update.stock_quantity == 25
    assert update.name is None


def test_product_update_empty_payload():

    update = ProductUpdate()

    assert update.name is None
    assert update.description is None
    assert update.price is None
    assert update.stock_quantity is None


def test_product_update_negative_price():

    with pytest.raises(ValidationError):

        ProductUpdate(
            price=-10,
        )


def test_product_update_zero_price():

    with pytest.raises(ValidationError):

        ProductUpdate(
            price=0,
        )


def test_product_update_negative_stock():

    with pytest.raises(ValidationError):

        ProductUpdate(
            stock_quantity=-10,
        )


def test_product_update_invalid_price():

    with pytest.raises(ValidationError):

        ProductUpdate(
            price="invalid",
        )


def test_product_update_invalid_stock():

    with pytest.raises(ValidationError):

        ProductUpdate(
            stock_quantity="abc",
        )


def test_product_update_empty_name():

    with pytest.raises(ValidationError):

        ProductUpdate(
            name="",
        )


def test_product_update_name_too_short():

    with pytest.raises(ValidationError):

        ProductUpdate(
            name="AB",
        )


def test_product_update_name_too_long():

    with pytest.raises(ValidationError):

        ProductUpdate(
            name="A" * 101,
        )


def test_product_update_description_too_long():

    with pytest.raises(ValidationError):

        ProductUpdate(
            description="A" * 501,
        )


def test_product_update_whitespace():

    update = ProductUpdate(
        name="     Gaming Mouse     ",
    )

    assert update.name == "Gaming Mouse"


# ==========================================================
# ProductResponse Tests
# ==========================================================

class MockProduct:
    id = 1
    name = "Keyboard"
    description = "RGB Keyboard"
    price = Decimal("99.99")
    stock_quantity = 10
    is_active = True
    created_at = datetime.now()
    updated_at = datetime.now()


def test_product_response_from_orm():

    response = ProductResponse.model_validate(MockProduct())

    assert response.id == 1
    assert response.name == "Keyboard"
    assert response.price == Decimal("99.99")
    assert response.stock_quantity == 10