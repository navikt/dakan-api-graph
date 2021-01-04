from typing import List
from data_catalog_api import store
from data_catalog_api.models.nodes import Node, NodeResponse
from data_catalog_api.models.requests import NodeRelationPayload
from data_catalog_api.utils import authentication
from fastapi import APIRouter
from data_catalog_api.log_metrics import metric_types
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from data_catalog_api.utils.logger import Logger

logger = Logger()
router = APIRouter()


@router.get("/node/{id}", response_model=NodeResponse, tags=["Node"])
@metric_types.REQUEST_TIME_GET_NODE_BY_ID.time()
def get_node_by_id(id: str):
    """
    Get node by id:

    - **id**: id of node
    """
    return store.get_node_by_id(id)


@router.get("/nodes/{label}", response_model=List[Node], tags=["Node"])
@metric_types.REQUEST_TIME_GET_NODE_BY_LABEL.time()
def get_nodes_by_label(label: str, skip: int = 0, limit: int = None, valid_nodes: bool = True):
    """
    Get nodes by label:

    - **label**: label of node
    """
    return store.get_nodes_by_label(label, skip, limit, valid_nodes)


@router.get("/node/out/{node_id}/{edge_label}", response_model=List[Node], tags=["Node"])
@metric_types.REQUESTS_TIME_GET_NODE_BY_OUTWARD_RELATION.time()
def get_out_nodes(node_id: str, edge_label: str, skip: int = 0, limit: int = None, valid_nodes: bool = True):
    """
    Get all nodes with outgoing relations to node_id

    - **node_id**: ID of node that has relations
    - **edge_label**: type of relation
    """
    return store.get_out_nodes(node_id, edge_label, skip, limit, valid_nodes)


@router.get("/node/in/{node_id}/{edge_label}", response_model=List[Node], tags=["Node"])
@metric_types.REQUESTS_TIME_GET_NODE_BY_INWARD_RELATION.time()
def get_in_nodes(node_id: str, edge_label: str, skip: int = 0, limit: int = None, valid_nodes: bool = True):
    """
    Get all nodes with incoming relations to node_id

    - **node_id**: ID of node that has relations
    - **edge_label**: type of relation
    """
    return store.get_in_nodes(node_id, edge_label, skip, limit, valid_nodes)


@router.put("/node", tags=["Node"])
@metric_types.REQUESTS_TIME_UPSERT_NODES.time()
def put_node(nodes: List[Node], request: Request):
    if authentication.is_authorized(request.headers):
        return store.upsert_node(nodes)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@router.put("/invalidate/nodes", tags=["Node"])
@metric_types.REQUESTS_TIME_INVALIDATE_NODES.time()
def put_node(node_ids: List[str], request: Request):
    if authentication.is_authorized(request.headers):
        return store.invalidate_nodes(node_ids)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@router.delete("/node/delete/id/{node_id}", tags=["Node"])
@metric_types.REQUESTS_TIME_DELETE_NODES.time()
def delete_node(node_id: str, request: Request):
    """
    - **node_id**: ID of node to delete
    """
    if authentication.is_authorized(request.headers):
        return store.delete_node(node_id)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@router.delete("/node/delete/type/{node_type}", tags=["Node"])
@metric_types.REQUESTS_TIME_DELETE_NODES_BY_TYPE.time()
def delete_node_type(node_type: str, request: Request):
    """
    - **node_type**: type of node to delete
    """
    if authentication.is_authorized(request.headers):
        return store.delete_node_by_type(node_type)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@router.put("/node/edge/upsert", tags=["Node"])
@metric_types.REQUESTS_TIME_UPSERT_NODE_AND_CREATE_EDGE.time()
def upsert_node_and_create_edge(payload: NodeRelationPayload, request: Request):
    """
    Creates a node based and generates an edge based on the payload

    - **payload**: Payload containing a node_body  to generate a new node,
                   and a source_id and edge_label to generate the relationship for the new node
    """
    if authentication.is_authorized(request.headers):
        return store.upsert_node_and_create_edge(payload)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"Error": "This operation requires authorization"})


@router.get("/nodes/test/{label}", tags=["Node"])
def get_nodes_by_label_test(label: str, page: int = 1, valid_nodes: bool = True):
    """
    Get nodes by label:

    - **label**: label of node
    """
    return store.get_nodes_by_label_test(label, page, valid_nodes)


@router.get("/nodes/test/term/{search_term}", tags=["Node"])
def get_nodes_by_label_test(search_term: str):
    """
    Get nodes by label:

    - **label**: label of node
    """
    return store.test_search(search_term)
