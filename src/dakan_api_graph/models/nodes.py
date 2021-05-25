from typing import Dict
from typing import List
from pydantic import BaseModel


class Node(BaseModel):
    id: str
    label: str
    properties: dict


class NodeResponse(Dict):
    id: str
    label: str
    type: str
    properties: dict


class PagedNodes(Dict):
    page: int
    total_pages: int
    has_next_page: bool
    max_items_per_page: int
    total_items: int
    data: List[Node]
