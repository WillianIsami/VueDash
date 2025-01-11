from fastapi import APIRouter
from app.api.v1.endpoints import recommendations, books, users

api_router = APIRouter()

api_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["recommendations"]
)
api_router.include_router(
    books.router,
    prefix="/books",
    tags=["books"]
)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)