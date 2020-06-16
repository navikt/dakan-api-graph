import prometheus_client
from fastapi import APIRouter, status
from fastapi.responses import Response

router = APIRouter()


@router.get("/metrics", include_in_schema=False)
def metrics():
    """
    Get metrics:

    """
    return Response(status_code=status.HTTP_200_OK, content=prometheus_client.generate_latest())
