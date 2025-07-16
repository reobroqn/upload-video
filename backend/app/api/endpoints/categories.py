from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryInDB

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryInDB, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate, db: Session = Depends(get_db)
) -> CategoryInDB:
    """
    Create a new category.
    """
    db_category = db.query(Category).filter(Category.name == category_in.name).first()
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists"
        )

    db_category = Category(name=category_in.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/", response_model=list[CategoryInDB])
async def get_all_categories(db: Session = Depends(get_db)) -> list[CategoryInDB]:
    """
    Get all categories.
    """
    return db.query(Category).all()


@router.get("/{category_id}", response_model=CategoryInDB)
async def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryInDB:
    """
    Get a category by ID.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category by ID.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    db.delete(category)
    db.commit()
    return
