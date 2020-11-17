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


@router.get("/edge/{id}", response_model=List[EdgeResponse], tags=["Edge"])
@metric_types.REQUEST_TIME_GET_EDGE_BY_ID.time()
def get_edge_by_id(id: str):
    """
    Get edge by id:

    - **id**: id of edge
    """
    return store.get_edge_by_id(id)


@router.get("/edge/label/{edge_label}", response_model=List[EdgeResponse], tags=["Edge"])
@metric_types.REQUEST_TIME_GET_EDGE_BY_LABEL.time()
def get_edge_by_label(edge_label: str):
    """
    Get edge by label:

    - **label**: label of edge
    """
    return store.get_edge_by_label(edge_label)


@router.put("/edge", tags=["Edge"])
@metric_types.REQUESTS_TIME_UPSERT_EDGES.time()
def put_edge(edges: List[Edge], request: Request):
    if authentication.is_authorized(request.headers):
        return store.upsert_edge(edges)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@router.delete("/edge", tags=["Edge"])
@metric_types.REQUESTS_TIME_DELETE_EDGES.time()
def delete_edge(n1: str, n2: str, request: Request):
    """
    Delete edge by n1 and n2

    - **n1**: ID of source node
    - **n2**: ID of target node
    """
    if authentication.is_authorized(request.headers):
        return store.delete_edge(n1, n2)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@router.delete("/edge/{label}", tags=["Edge"])
@metric_types.REQUESTS_TIME_DELETE_EDGES_BY_LABEL.time()
def delete_edge(label: str, request: Request):
    """
    Delete edge by label

    - **label**: Edge label
    """
    if authentication.is_authorized(request.headers):
        return store.delete_edge_by_label(label)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@router.delete("/edges/all/{node_id}", tags=["Edge"])
@metric_types.REQUESTS_TIME_DELETE_ALL_EDGES_OF_NODE.time()
def delete_all_edge_of_node(node_id: str, request: Request):
    """
    Delete all edges of a node

    - **node_id**: Id of node
    """
    if authentication.is_authorized(request.headers):
        return store.delete_all_edges_of_node(node_id)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})
