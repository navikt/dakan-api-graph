from pydantic import BaseModel
from data_catalog_api.models.nodes import Node


class CommentPayload(BaseModel):
    source_id: str
    edge_label: str
    comment_body: Node
