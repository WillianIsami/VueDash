from typing import List, Optional
from fastapi import HTTPException
from app.core.config import settings
from app.models.schemas import RecommendationResponse
from app.ml_models.book_recommender import BookRecommender

class RecommendationService:
    _instance: Optional['RecommendationService'] = None
    _model: Optional[BookRecommender] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_model(cls) -> BookRecommender:
        if cls._model is None:
            try:
                cls._model = BookRecommender.load_model(settings.MODEL_PATH)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to load recommendation model: {str(e)}"
                )
        return cls._model

    @classmethod
    async def get_similar_books(
        cls, isbn: str, limit: int = 5, offset: int = 0
    ) -> List[RecommendationResponse]:
        model = cls.get_model()
        try:
            recommendations = model.get_similar_books(isbn, limit, offset)
            return [
                RecommendationResponse(
                    isbn=rec['ISBN'],
                    title=rec['Title'],
                    author=rec['Author'],
                    year=rec['Year'],
                    image_small=rec['Image-URL-S'],
                    image_medium=rec['Image-URL-M'],
                    image_large=rec['Image-URL-L'],
                    similarity_score=rec['Similarity Score'],
                )
                for rec in recommendations
            ]
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Error getting recommendations: {str(e)}"
            )
        
    @classmethod
    async def recommend_for_new_user(
        cls, limit: int = 5, offset: int = 0
    ) -> List[RecommendationResponse]:
        model = cls.get_model()
        try:
            recommendations = model.recommend_for_new_user(limit, offset)
            return [
                RecommendationResponse(
                    isbn=rec['ISBN'],
                    title=rec['Title'],
                    author=rec['Author'],
                    year=rec['Year'],
                    image_small=rec['Image-URL-S'],
                    image_medium=rec['Image-URL-M'],
                    image_large=rec['Image-URL-L'],
                )
                for rec in recommendations
            ]
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Error getting recommendations: {str(e)}"
            )

    @classmethod
    async def get_user_recommendations(
        cls, user_id: int, limit: int = 5, offset: int = 0
    ) -> List[RecommendationResponse]:
        model = cls.get_model()
        try:
            recommendations = model.get_user_recommendations(user_id, limit, offset)
            return [
                RecommendationResponse(
                    isbn=rec['ISBN'],
                    title=rec['Title'],
                    author=rec['Author'],
                    year=rec['Year'],
                    image_small=rec['Image-URL-S'],
                    image_medium=rec['Image-URL-M'],
                    image_large=rec['Image-URL-L'],
                    predicted_rating=rec['Predicted Rating'],
                )
                for rec in recommendations
            ]
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Error getting recommendations: {str(e)}"
            )
