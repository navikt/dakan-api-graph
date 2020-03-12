import logging
import os

from data_catalog_api.models.edges import Edge
from data_catalog_api.models.nodes import Node
from data_catalog_api.models.requests import CommentPayload
from dotenv import load_dotenv
from fastapi import status
from fastapi.responses import JSONResponse
from gremlin_python.driver import client, serializer
from data_catalog_api.exceptions.exceptions import MultipleNodesInDbError

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def setup_cosmosdb_con():
    return os.environ["cosmosDBConnection"], client.Client(os.environ["cosmosDBServer"], 'g',
                              username=os.environ["cosmosDBUsername"],
                              password=os.environ["cosmosDBPassword"],
                              message_serializer=serializer.GraphSONSerializersV2d0())

# CosmosDB does not support bytecode yet
# https://github.com/Azure/azure-cosmos-dotnet-v2/issues/439
""" def setup_graph():
    try:
        graph = Graph()
        g = graph.traversal().withRemote(DriverRemoteConnection(connstring, 'gmodern'))
        logging.info('Successfully logged in to CosmosDB')
    except Exception as e: 
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail="Could not Login to CosmosDB")
    return g """

try:
    connstring, cosmosdb_conn = setup_cosmosdb_con()
except KeyError:
    logging.warning("Getting env variables from .env file")
    load_dotenv()
    connstring, cosmosdb_conn = setup_cosmosdb_con()


def submit(query, message=None, params=None):
    callback = cosmosdb_conn.submitAsync(query)
    results = []
    if callback.result() is not None:
        for result in callback.result():
            results.extend(result)
        return results
    else:
        print(f"No results returned from query: {query}")


async def get_node_by_id(node_id: str):
    res = submit(f"g.V('{node_id}')")

    if len(res) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    if len(res) > 1:
        raise MultipleNodesInDbError(node_id)
    else:
        return res[0]


async def get_nodes_by_label(label: str, skip: int, limit: int):
    if limit is None:
        return submit(f"g.V().hasLabel('{label}')")

    return submit(f"g.V().hasLabel('{label}').range({skip}, {skip+limit})")


async def upsert_node(node: Node):
    params = ""
    for key, value in node.properties.items():
        params = f"{params}.property('{key}','{value}')"

    query = f"g.V().has('label','{node.label}').has('id','{node.id}').fold().coalesce(unfold(){params}," \
            f"addV('{node.label}').property('id','{node.id}').property('version','1'){params})"

    res = submit(query)
    return res


async def get_out_nodes(node_id: str, edge_label: str):
    return submit(f"g.V('{node_id}').out('{edge_label}')")


async def get_in_nodes(node_id: str, edge_label: str):
    return submit(f"g.V('{node_id}').in('{edge_label}')")


async def get_edge_by_id(id: str):
    query = f"g.E('{id}')"
    return submit(query)


async def create_edge(edge: Edge):
    query = f"g.V('{edge.inV}').addE('{edge.label}').to(g.V('{edge.outV}'))"
    return submit(query)


async def upsert_comment(payload: CommentPayload):
    node = payload.comment_body
    params = ""
    for key, value in node.properties.items():
        params = f"{params}.property('{key}','{value}')"

    query = f"g.V().has('label','{node.label}').has('id','{node.id}').fold().coalesce(unfold(){params}," \
            f"addV('{node.label}').property('id','{node.id}').property('version','1'){params}); "
    submit(query)
    query_generate_edge = f"g.V('{payload.source_id}').addE('{payload.edge_label}').to(g.V('{node.id}'))"

    return submit(query_generate_edge)


async def delete_node(source_id: str, target_id: str):
    query_delete_edge = f"g.V('{source_id}').outE().where(outV().hasId('{target_id}')).drop()"
    submit(query_delete_edge)
    query_delete_node = f"g.V('{target_id}').drop()"
    return submit(query_delete_node)
