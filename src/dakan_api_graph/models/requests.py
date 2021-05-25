from pydantic import BaseModel
from dakan_api_graph.models.nodes import Node


class NodeRelationPayload(BaseModel):
    source_id: str
    edge_label: str
    node_body: Node
