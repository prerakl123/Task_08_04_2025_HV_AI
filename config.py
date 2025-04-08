import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class Config:
    """Config class for Flask application."""
    # Flask secret key for session management
    SECRET_KEY = os.environ.get("SECRET_KEY", "some-random-secret-key")

    # Secret key for JWT authentication
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    # Expiration time for JWT access tokens (in seconds)
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    # Database connection URI
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
