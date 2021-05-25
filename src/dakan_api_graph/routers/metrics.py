import prometheus_client as pc
from fastapi import APIRouter, status
from starlette.responses import Response

router = APIRouter()


@router.get("/metrics", include_in_schema=False)
def metrics():
    """
    Get metrics:

    """
    headers = {'Content-Type': pc.CONTENT_TYPE_LATEST}
    return Response(pc.generate_latest(pc.REGISTRY), status_code=status.HTTP_200_OK, headers=headers)
