from __future__ import annotations

from typing import Iterable

from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import PyMongoError

from ..models.team import TeamMember, TeamSubmission
from ..utils.mongo import db
from .mail_service import send_welcome_email_task


collection = db["hackathon_teams"]


async def ensure_no_existing_member(members: Iterable[TeamMember]) -> None:
    emails = [member.email_id for member in members]
    regs = [member.registration_number for member in members]

    query = {
        "$or": [
            {"members.email_id": {"$in": emails}},
            {"members.registration_number": {"$in": regs}},
        ]
    }
    if await collection.count_documents(query):
        raise HTTPException(
            status_code=409,
            detail="One of the provided emails or registration numbers is already registered.",
        )


async def ensure_unique_transaction(transaction_id: str) -> None:
    """Prevent inserting a team with the same transaction id twice."""
    query = {"transaction_id": transaction_id}
    if await collection.count_documents(query):
        raise HTTPException(
            status_code=409,
            detail="Duplicate transaction ID found.",
        )


async def register_team(team: TeamSubmission) -> ObjectId:
    try:
        await ensure_no_existing_member(team.members)
        await ensure_unique_transaction(team.transaction_id)
        team_doc = team.dict()
        team_doc["leader_email"] = team.members[0].email_id
        insert_result = await collection.insert_one(team_doc)
        send_welcome_email_task.delay(team.members[0].email_id, team.members[0].name)
        return insert_result.inserted_id
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="MongoDB unavailable.") from exc


async def list_teams() -> list[dict]:
    try:
        cursor = collection.find().sort("_id", -1)
        teams = []
        async for document in cursor:
            document["_id"] = str(document["_id"])
            teams.append(document)
        return teams
    except PyMongoError as exc:
        raise HTTPException(status_code=503, detail="MongoDB unavailable.") from exc
