from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.backend.models.response import ResponsePayload
from app.backend.services.response_service import save_response

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1", tags=["responses"])


@router.post("/responses", summary="Store frontend response data to MongoDB")
async def create_response(payload: ResponsePayload) -> dict[str, str]:
    try:
        data = payload.dict(exclude_none=True)
        inserted_id = await save_response(data)
        logger.debug("Payload saved, returning identifier.")
        return {"status": "success", "inserted_id": str(inserted_id)}
    except Exception as exc:
        logger.exception("Failed to save frontend response: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Unable to save response at this time. Please retry later.",
        )
