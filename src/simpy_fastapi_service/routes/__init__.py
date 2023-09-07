from fastapi import APIRouter

from simpy_fastapi_service.routes import health, simulation

router = APIRouter()
health_router = APIRouter()

health_router.include_router(
    health.router,
    prefix="",
)

router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
