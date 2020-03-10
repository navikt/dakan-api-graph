from pydantic import BaseModel


class Edge(BaseModel):
    label: str
    inV: str
    outV: str


class EdgeResponse(BaseModel):
    id: str
    label: str
    type: str
    inV: str
    outV: str
    inVLabel: str
    outVLabel: str
