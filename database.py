from sqlmodel import create_engine, Session
from pydantic_settings import BaseSettings

# Define settings for the application
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./caching_service.db"  # Default SQLite URL

    class ConfigDict:
        env_file = ".env"  # Load environment variables from .env file

# Load settings
settings = Settings()

# Create the database engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Function to get a database session
def get_session():
    with Session(engine) as session:
        yield session

