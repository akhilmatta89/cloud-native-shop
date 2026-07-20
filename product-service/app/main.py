"""
Task: CNS_2.5
Product Service Entry Point
"""

from fastapi import FastAPI

from app.routes import router


app = FastAPI(
    title="Product Service",
    version="1.0.0",
    description="Cloud Native Shop - Product Service",
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "product-service",
    }