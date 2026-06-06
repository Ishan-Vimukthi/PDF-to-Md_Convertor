from fastapi import FastAPI

from app.core.config import settings
from app.api.endpoints import router as conversion_router


def create_application() -> FastAPI:
    """
    Application factory for creating the FastAPI instance.
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
    )

    # Include API routers
    application.include_router(conversion_router)

    return application


app = create_application()


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "healthy", "service": "pdf2md-converter"}
