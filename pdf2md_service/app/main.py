from fastapi import FastAPI

from app.core.config import settings


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

    # Include routers here in Phase 2
    # from app.api.routes import router as api_router
    # application.include_router(api_router, prefix="/api/v1")

    return application


app = create_application()


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "healthy", "service": "pdf2md-converter"}
