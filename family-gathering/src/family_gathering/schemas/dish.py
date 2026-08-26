from pydantic import BaseModel, Field

from family_gathering.models import DishStatus


class DishOut(BaseModel):
    id: str
    name: str
    claimed_by: str | None
    servings: str
    status: DishStatus


class DishCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    servings: str = Field(default="", max_length=100)


class DishClaim(BaseModel):
    participant_id: str = Field(min_length=1)
