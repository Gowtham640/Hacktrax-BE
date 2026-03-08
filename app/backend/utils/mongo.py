from __future__ import annotations

import logging

from motor.motor_asyncio import AsyncIOMotorClient

from app.backend import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

logger.info("Initializing MongoDB client for database %s", config.DATABASE_NAME)
client = AsyncIOMotorClient(config.MONGO_URI)
db = client[config.DATABASE_NAME]
