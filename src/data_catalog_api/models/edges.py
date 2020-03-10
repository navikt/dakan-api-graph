from pydantic import BaseModel


class Edge(BaseModel):
    id: str
    label: str
    inV: str
    outV: str
    inVlabel: str
    outVlabel: str


class EdgeResponse(BaseModel):
    id: str
    label: str
    type: str
    properties: dict
