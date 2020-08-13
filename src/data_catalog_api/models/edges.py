from pydantic import BaseModel


class Edge(BaseModel):
    """
    label: relation type
    inV: source node being pointed at
    outV: source node pointing to
    """
    label: str
    inV: str
    outV: str
    properties: dict = {}


class EdgeResponse(BaseModel):
    id: str
    label: str
    type: str
    inV: str
    outV: str
    inVLabel: str
    outVLabel: str
    properties: dict = {}
