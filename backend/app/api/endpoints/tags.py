from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagInDB

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/", response_model=TagInDB, status_code=status.HTTP_201_CREATED)
async def create_tag(tag_in: TagCreate, db: Session = Depends(get_db)) -> TagInDB:
    """
    Create a new tag.
    """
    db_tag = db.query(Tag).filter(Tag.name == tag_in.name).first()
    if db_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists"
        )

    db_tag = Tag(name=tag_in.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.get("/", response_model=list[TagInDB])
async def get_all_tags(db: Session = Depends(get_db)) -> list[TagInDB]:
    """
    Get all tags.
    """
    return db.query(Tag).all()


@router.get("/{tag_id}", response_model=TagInDB)
async def get_tag(tag_id: int, db: Session = Depends(get_db)) -> TagInDB:
    """
    Get a tag by ID.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Delete a tag by ID.
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    db.delete(tag)
    db.commit()
    return
