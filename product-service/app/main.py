from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routes import router
from app.exceptions import ProductNotFoundException

app = FastAPI(
    title="Product Service",
    version="1.0.0",
    description="Cloud Native Shop - Product Service",
)

app.include_router(router)


@app.exception_handler(ProductNotFoundException)
async def product_not_found_exception_handler(
    request: Request,
    exc: ProductNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "product-service",
    }