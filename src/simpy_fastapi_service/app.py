from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

from simpy_fastapi_service import routes
from simpy_fastapi_service.settings import Settings
from simpy_fastapi_service.version import __version__


def get_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        default_response_class=ORJSONResponse,
        version=__version__,
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Configure the main router
    app.include_router(routes.router, prefix="")

    # Configure the unprotected health router
    app.include_router(
        routes.health_router,
        prefix="",
    )

    return app
