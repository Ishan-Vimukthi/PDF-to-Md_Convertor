from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    PROJECT_NAME: str = "PDF to Markdown Converter"
    PROJECT_DESCRIPTION: str = (
        "A highly accurate PDF to Markdown conversion microservice powered by docling."
    )
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
