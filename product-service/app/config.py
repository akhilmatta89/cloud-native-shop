import os


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://shop_user:shop_password@localhost:5432/shop"
    )
    LOG_LEVEL: str = "INFO"

settings = Settings()