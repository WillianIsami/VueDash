from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    year_published: int
    publisher: str

class UserBase(BaseModel):
    user_id: str
    location: str
    age: str

class RecommendationResponse(BaseModel):
    isbn: str
    title: str
    author: str
    year: int
    similarity_score: Optional[float] = None
    predicted_rating: Optional[float] = None