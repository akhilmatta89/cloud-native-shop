""" Task:CNS_2.4
Create route module for managing products. """

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.services import ProductService

router = APIRouter()


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create_product(db, product)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.get_product_by_id(db, product_id)


@router.get("/products", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return ProductService.get_all_products(db)


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    return ProductService.update_product(db, product_id, product_update)


@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService.delete_product(db, product_id)