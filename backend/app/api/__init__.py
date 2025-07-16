from datetime import datetime

from fastapi import APIRouter

from app.api.endpoints import auth, categories, tags, users, videos

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(videos.router, tags=["videos"])
api_router.include_router(tags.router, tags=["tags"])
api_router.include_router(categories.router, tags=["categories"])

__all__ = ["api_router"]
