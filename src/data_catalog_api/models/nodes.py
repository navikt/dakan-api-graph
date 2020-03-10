from pydantic import BaseModel


class Node(BaseModel):
    id: str
    label: str
    properties: dict


class NodeResponse(BaseModel):
    id: str
    label: str
    type: str
    properties: dict
