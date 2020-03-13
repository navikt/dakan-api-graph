import prometheus_client
from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics", include_in_schema=False)
async def get_node_by_id():
    """
    Get node by id:

    - **id**: id of node
    """
    return await prometheus_client.generate_latest()
