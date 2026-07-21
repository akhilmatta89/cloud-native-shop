import logging

import app.config

logging.basicConfig(
    level=app.config.settings.LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

logger = logging.getLogger("product-service")