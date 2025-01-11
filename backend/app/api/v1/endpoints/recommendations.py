from fastapi import APIRouter, Query, Depends
from typing import List
from app.models.schemas import RecommendationResponse
from app.services.recommendation import RecommendationService

router = APIRouter()

@router.get("/similar/{isbn}", response_model=List[RecommendationResponse])
async def get_similar_books(
    isbn: str,
    limit: int = Query(default=5, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    recommendation_service: RecommendationService = Depends(RecommendationService)
):
    """
    Get similar books based on ISBN
    """
    return await recommendation_service.get_similar_books(isbn, limit, offset)

@router.get("/user/{user_id}", response_model=List[RecommendationResponse])
async def get_user_recommendations(
    user_id: int,
    limit: int = Query(default=5, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    recommendation_service: RecommendationService = Depends(RecommendationService)
):
    """
    Get personalized recommendations for a user
    """
    return await recommendation_service.get_user_recommendations(user_id, limit, offset)
