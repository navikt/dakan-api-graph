from typing import List
from data_catalog_api import store
from data_catalog_api.models.nodes import Node, NodeResponse
from data_catalog_api.models.requests import CommentPayload
from fastapi import APIRouter

router = APIRouter()


@router.get("/node/{id}", response_model=NodeResponse, tags=["Node"])
async def get_node_by_id(id: str):
    """
    Get node by id:

    - **id**: id of node
    """
    return await store.get_node_by_id(id)


@router.get("/nodes/{label}", response_model=List[Node], tags=["Node"])
async def get_nodes_by_label(label: str, skip: int=0, limit: int=None):
    """
    Get nodes by label:

    - **label**: label of node
    """
    return await store.get_nodes_by_label(label, skip, limit)


@router.get("/node/out/{node_id}/{edge_label}", response_model=List[Node], tags=["Node"])
async def get_out_nodes(node_id: str, edge_label: str):
    return await store.get_out_nodes(node_id, edge_label)


@router.get("/node/in/{node_id}/{edge_label}", response_model=List[Node], tags=["Node"])
async def get_in_nodes(node_id: str, edge_label: str):
    return await store.get_in_nodes(node_id, edge_label)


@router.put("/node", tags=["Node"])
async def put_node(node: Node):
    return await store.upsert_node(node)


@router.put("/node/add/comment", tags=["Node"])
async def put_node_comment(payload: CommentPayload):
    return await store.upsert_comment(payload)
