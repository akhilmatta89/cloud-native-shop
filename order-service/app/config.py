from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Order Service"
    APP_VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str

    # Product Service (used for service-to-service communication)
    PRODUCT_SERVICE_URL: str = "http://product-service:8000"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()