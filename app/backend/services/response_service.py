from __future__ import annotations

import logging

from bson import ObjectId

from ..utils.mongo import db

logger = logging.getLogger(__name__)


async def save_response(payload: dict) -> ObjectId:
    collection = db["frontend_responses"]
    logger.debug("Saving payload to MongoDB collection %s", collection.name)
    insert_result = await collection.insert_one(payload)
    logger.info("Inserted document with id %s into %s", insert_result.inserted_id, collection.name)
    return insert_result.inserted_id
