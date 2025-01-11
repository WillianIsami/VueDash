from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    year_published: int
    publisher: str
    image_small: str
    image_medium: str
    image_large: str

class UserBase(BaseModel):
    user_id: str
    location: str
    age: str

class RecommendationResponse(BaseModel):
    isbn: str
    title: str
    author: str
    year: int
    image_small: str
    image_medium: str
    image_large: str
    similarity_score: Optional[float] = None
    predicted_rating: Optional[float] = None