from pydantic import BaseModel, Field


class MetaOut(BaseModel):
    title: str
    when: str
    where: str
    note: str
