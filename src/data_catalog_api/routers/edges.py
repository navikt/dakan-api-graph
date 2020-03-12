from typing import List
from data_catalog_api import store
from data_catalog_api.models.edges import Edge, EdgeResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/edge/{id}", response_model=List[EdgeResponse], tags=["Edge"])
async def get_edge_by_id(id: str):
    """
    Get node by id:

    - **id**: id of node
    """
    return await store.get_edge_by_id(id)


@router.put("/edge", tags=["Edge"])
async def put_node(edge: Edge):
    return await store.create_edge(edge)


@router.delete("/edge/delete", tags=["Edge"])
async def delete_edge(n1: str, n2: str):
    return await store.delete_edge(n1, n2)
