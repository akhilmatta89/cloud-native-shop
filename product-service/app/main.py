from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float

products = []

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/products")
def get_products():
    products.append({"id":1,"name":"samsung","price":3000.00})
    products.append({"id": 2, "name": "apple", "price": 5000.00})
    return products

@app.get("/products/{id}", response_model=Product)
def get_product(id):
    for product in products:
        if str(product["id"]) == id:
            return product
    raise HTTPException(
        status_code=404,
        detail=f"product-id: {id} not found"
    )