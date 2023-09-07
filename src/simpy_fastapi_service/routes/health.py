from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    """Retrieve status for health checks"""
    return {"status": "OK"}
