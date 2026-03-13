from __future__ import annotations

from typing import Iterable, List

from pydantic import BaseModel, EmailStr, Field, constr, model_validator, validator


class TeamMember(BaseModel):
    name: str = Field(..., description="Full name of the team member.")
    email_id: EmailStr = Field(..., description="SRM email used for registration.")
    phone_number: constr(pattern=r"^\d{10}$") = Field(..., description="10-digit contact number.")
    registration_number: constr(pattern=r"^RA\d{13}$") = Field(
        ..., description="SRM registration number prefixed with RA."
    )

    @validator("email_id")
    def ensure_srm_domain(cls, value: EmailStr) -> EmailStr:
        if not value.endswith("@srmist.edu.in"):
            raise ValueError("Email must end with '@srmist.edu.in'.")
        return value


class TeamSubmission(BaseModel):
    team_name: str = Field(..., description="Unique team name.")
    members: List[TeamMember] = Field(
        ...,
        description="Ordered list of up to four students; first member is the leader.",
        min_items=1,
        max_items=4,
    )
    transaction_id: str = Field(..., description="Transaction ID of the payment.")

    @model_validator(mode="after")
    def ensure_unique_members(cls, values: "TeamSubmission") -> "TeamSubmission":
        members: Iterable[TeamMember] = values.members
        seen_emails = set()
        seen_regs = set()
        for member in members:
            if member.email_id in seen_emails:
                raise ValueError(f"Duplicate email in team: {member.email_id}")
            seen_emails.add(member.email_id)

            if member.registration_number in seen_regs:
                raise ValueError(f"Duplicate registration number in team: {member.registration_number}")
            seen_regs.add(member.registration_number)
        return values
