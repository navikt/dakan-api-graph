from typing import List
from data_catalog_api import store
from data_catalog_api.models.edges import Edge, EdgeResponse
from fastapi import APIRouter
from data_catalog_api.log_metrics import metric_types


router = APIRouter()


@router.get("/edge/{id}", response_model=List[EdgeResponse], tags=["Edge"])
@metric_types.REQUEST_TIME_GET_EDGE_BY_ID.time()
async def get_edge_by_id(id: str):
    """
    Get edge by id:

    - **id**: id of edge
    """
    return await store.get_edge_by_id(id)


@router.put("/edge", tags=["Edge"])
@metric_types.REQUESTS_TIME_UPSERT_EDGES.time()
async def put_node(edges: List[Edge]):
    return await store.create_edge(edges)


@router.delete("/edge/delete", tags=["Edge"])
@metric_types.REQUESTS_TIME_DELETE_EDGES.time()
async def delete_edge(n1: str, n2: str):
    """
    Delete edge by n1 and n2

    - **n1**: ID of source node
    - **n2**: ID of target node
    """
    return await store.delete_edge(n1, n2)
