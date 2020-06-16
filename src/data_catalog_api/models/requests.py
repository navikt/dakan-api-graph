from pydantic import BaseModel
from data_catalog_api.models.nodes import Node


class NodeRelationPayload(BaseModel):
    source_id: str
    edge_label: str
    node_body: Node
