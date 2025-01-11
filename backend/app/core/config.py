from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_NAME: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # Data paths
    RAW_DATA_PATH: str = "app/data/raw"
    FILTERED_DATA_PATH: str = "app/data/filtered"

    PROJECT_NAME: str = "Book Recommendation System"
    MODEL_PATH: str = "app/ml_models/trained_models/recommender_model.pkl"
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()