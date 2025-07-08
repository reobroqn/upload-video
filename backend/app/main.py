from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance

    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Backend API for VideoFlow - A video upload and streaming service",
        docs_url=None,  # Disable default Swagger UI
        redoc_url=None,  # Disable default ReDoc
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # Configure CORS
    setup_cors(app)

    # Include API routes
    setup_routes(app)

    return app


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the application.

    Args:
        app: The FastAPI application instance

    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_routes(app: FastAPI) -> None:
    """
    Set up all API routes and endpoints.

    Args:
        app: The FastAPI application instance

    """
    # Include API v1 routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        """
        Root endpoint that returns a welcome message.

        Returns:
            dict: A welcome message

        """
        return {"message": "Welcome to VideoFlow API"}

    @app.get("/health", include_in_schema=False)
    async def health_check() -> dict[str, str]:
        """
        Health check endpoint.

        Returns:
            dict: Status of the API service

        """
        return {"status": "ok"}

    # Custom Swagger UI
    @app.get(f"{settings.API_V1_STR}/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{settings.PROJECT_NAME} - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    # OpenAPI JSON
    @app.get(app.openapi_url[1:], include_in_schema=False)
    async def get_open_api_endpoint():
        return JSONResponse(
            get_openapi(
                title=app.title,
                version=app.version,
                routes=app.routes,
            )
        )


# Create the FastAPI application
app = create_application()
