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
    response = await store.get_edge_by_id(id)
    return response


@router.put("/edge", tags=["Edge"])
async def put_node(edge: Edge):
    response = await store.create_edge(edge)
    return response
