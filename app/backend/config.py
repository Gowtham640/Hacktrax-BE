from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI must be set in the environment.")

DATABASE_NAME = os.getenv("MONGO_DB_NAME", "alexa")
PASSWORD = os.getenv("PASSWORD")
if not PASSWORD:
    raise RuntimeError("PASSWORD must be set in the environment.")

logger.info("Configuration loaded: database=%s", DATABASE_NAME)
