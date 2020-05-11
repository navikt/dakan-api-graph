from typing import List
from data_catalog_api import store
from data_catalog_api.models.edges import Edge, EdgeResponse
from data_catalog_api.utils import authentication
from fastapi import APIRouter
from data_catalog_api.log_metrics import metric_types
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

router = APIRouter()


@metric_types.REQUEST_TIME_GET_EDGE_BY_ID.time()
@router.get("/edge/{id}", response_model=List[EdgeResponse], tags=["Edge"])
async def get_edge_by_id(id: str):
    """
    Get edge by id:

    - **id**: id of edge
    """
    return await store.get_edge_by_id(id)


@metric_types.REQUESTS_TIME_UPSERT_EDGES.time()
@router.put("/edge", tags=["Edge"])
async def put_edge(edges: List[Edge], request: Request):
    if authentication.is_authorized(request.headers):
        return await store.upsert_edge(edges)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@metric_types.REQUESTS_TIME_DELETE_EDGES.time()
@router.delete("/edge", tags=["Edge"])
async def delete_edge(n1: str, n2: str, request: Request):
    """
    Delete edge by n1 and n2

    - **n1**: ID of source node
    - **n2**: ID of target node
    """
    if authentication.is_authorized(request.headers):
        return await store.delete_edge(n1, n2)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})
