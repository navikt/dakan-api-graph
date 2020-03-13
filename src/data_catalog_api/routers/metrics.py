import prometheus_client
from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics", include_in_schema=False)
def metrics():
    """
    Get metrics:

    """

    return prometheus_client.generate_latest()
