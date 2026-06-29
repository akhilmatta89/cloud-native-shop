from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()
PRODUCT_SERVICE_URL = "http://localhost:8001"

class OrderRequest(BaseModel):
    product_id: int
    quantity: int

class ProdResponse(BaseModel):
    id: int
    name: str
    price: float

class OrderResponse(BaseModel):
    order_id: int
    product: ProdResponse
    quantity: int
    total_price: float

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/orders", response_model=OrderResponse)
def orders(order_request: OrderRequest):
    url = f"{PRODUCT_SERVICE_URL}/products/{order_request.product_id}"
    try:
        req = requests.get(url, timeout=5)
        req.raise_for_status()
    except requests.exceptions.HTTPError:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Product service unavailable"
        )
    response_from_product_service = req.json()
    return {
        "order_id": 1,
        "product": response_from_product_service,
        "quantity": order_request.quantity,
        "total_price": response_from_product_service["price"] * order_request.quantity
    }
