from pydantic import BaseModel, Field

from family_gathering.models import ParticipantStatus


class ParticipantOut(BaseModel):
    id: str
    name: str
    headcount: int
    status: ParticipantStatus
    note: str


class ParticipantCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    headcount: int = Field(default=1, ge=1, le=20)
    status: ParticipantStatus = ParticipantStatus.COMING
    note: str = Field(default="", max_length=200)


class ParticipantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    headcount: int | None = Field(default=None, ge=1, le=20)
    status: ParticipantStatus | None = None
    note: str | None = Field(default=None, max_length=200)
