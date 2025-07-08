from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings and configuration.

    Settings are loaded from environment variables with the following hierarchy:
    1. Environment variables
    2. .env file
    3. Default values (if specified)

    Attributes:
        PROJECT_NAME: Name of the project
        VERSION: Current version of the application
        API_V1_STR: Base path for API version 1 endpoints

    """

    PROJECT_NAME: str = "VideoFlow"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def database_url(self) -> str:
        """
        Construct and return the database connection URL.

        Combines the database connection parameters into a valid SQLAlchemy URL.

        Returns:
            str: A SQLAlchemy-compatible database URL

        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_TYPE: str = "bearer"  # Token type for WWW-Authenticate header

    # AWS Configuration
    # AWS_ACCESS_KEY_ID: str
    # AWS_SECRET_ACCESS_KEY: str
    # AWS_REGION: str
    # AWS_S3_BUCKET: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        """
        Pydantic configuration.

        Configures how Pydantic loads and validates settings.
        """

        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Get the application settings with caching.

    This function uses lru_cache to ensure settings are only loaded once per process,
    improving performance by avoiding repeated environment variable lookups.

    Returns:
        Settings: A cached instance of the application settings

    """
    return Settings()


settings = get_settings()
