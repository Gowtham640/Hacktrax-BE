from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ResponsePayload(BaseModel):
    user_id: str = Field(..., description="Identifier for the user sending responses.")
    session_id: str = Field(..., description="Identifier for the frontend session.")
    answers: Dict[str, Any] = Field(..., description="Structured answers keyed by question.")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Optional metadata such as device info or browser data."
    )
    captured_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp captured server-side if the client omits it.",
    )
