import httpx

from app.config import settings

class ProductClient:

    @staticmethod
    def get_product(product_id: int) -> dict:
        """
        Fetch product details from Product Service.
        """
        # Implement _get_product() using httpx to call the Product Service.
        url = f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}"
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def reduce_inventory(product_id: int, new_stock: int) -> dict:
        """
        Update the product inventory in Product Service.
        """
        url = f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}"

        payload = {
            "stock_quantity": new_stock
        }

        response = httpx.put(
            url,
            json=payload,
            timeout=10.0,
        )

        response.raise_for_status()

        return response.json()