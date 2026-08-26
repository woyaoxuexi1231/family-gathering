from pydantic import BaseModel, Field

from family_gathering.schemas.participant import ParticipantOut


class SignupTaskOut(BaseModel):
    id: str
    name: str


class SignupOut(BaseModel):
    participant: ParticipantOut
    task: SignupTaskOut | None = None


class SignupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    task: str = Field(min_length=1, max_length=80)
    headcount: int = Field(default=1, ge=1, le=20)
    note: str = Field(default="", max_length=200)
