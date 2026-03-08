from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.backend.models.team import TeamSubmission
from app.backend.services.team_service import list_teams, register_team

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1", tags=["teams"])


@router.post("/teams", summary="Register a hackathon team with validated members.")
async def create_team(team: TeamSubmission) -> dict[str, str]:
    try:
        team_id = await register_team(team)
        logger.info("Team %s registered with leader %s", team.team_name, team.members[0].email_id)
        return {"status": "success", "team_id": str(team_id)}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error while registering team: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Unable to register team at the moment. Please retry later.",
        )


@router.get("/teams", summary="List all registered teams.")
async def get_teams() -> dict[str, list[dict]]:
    teams = await list_teams()
    return {"teams": teams}
