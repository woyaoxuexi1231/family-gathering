from pydantic import BaseModel, Field


class EntryOut(BaseModel):
    id: str
    name: str
    dish: str
    headcount: int
    note: str


class EntryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    dish: str = Field(min_length=1, max_length=80)
    headcount: int = Field(default=1, ge=1, le=20)
    note: str = Field(default="", max_length=200)
