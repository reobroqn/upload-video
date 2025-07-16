from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., description="Name of the tag")


class TagCreate(TagBase):
    pass


class TagInDB(TagBase):
    id: int = Field(..., description="Tag ID")

    class Config:
        from_attributes = True
