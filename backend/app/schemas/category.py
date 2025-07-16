from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., description="Name of the category")


class CategoryCreate(CategoryBase):
    pass


class CategoryInDB(CategoryBase):
    id: int = Field(..., description="Category ID")

    class Config:
        from_attributes = True
