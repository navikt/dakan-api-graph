import math
from typing import List

from data_catalog_api import store
from data_catalog_api.models.nodes import Node, NodeResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/node/{id}", response_model=NodeResponse)
async def get_node_by_id(id: str):
    """
    Get node by id:

    - **id**: id of node
    """
    response = await store.get_node_by_id(id)
    return response


@router.get("/nodes/{label}", response_model=List[Node])
async def get_nodes_by_label(label: str, skip: int=0, limit: int=None):
    """
    Get nodes by label:

    - **label**: label of node
    """
    response = await store.get_nodes_by_label(label, skip, limit)
    return response


# @router.get("/linkednodes/{id}", response_model=List[Node])
# async def get_linked_nodes(id: str, edge_label)


@router.put("/node")
async def put_node(node: Node):
    response = await store.upsert_node(node)
    return response
