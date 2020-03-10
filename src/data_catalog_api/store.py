import logging
import os
import ast

from data_catalog_api.models.nodes import Node
from dotenv import load_dotenv
from fastapi import status
from fastapi.responses import JSONResponse
from gremlin_python.driver import client, serializer
from data_catalog_api.exceptions.exceptions import MultipleNodesInDbError

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


load_dotenv()
connstring = os.environ.get("cosmosDBConnection")

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

cosmosdb_conn = client.Client(os.environ.get("cosmosDBServer"), 'g',
                              username=os.environ.get("cosmosDBUsername"),
                              password=os.environ.get("cosmosDBPassword"),
                              message_serializer=serializer.GraphSONSerializersV2d0())


def submit(query, message=None, params=None):
    callback = cosmosdb_conn.submitAsync(query)
    results = []
    if callback.result() is not None:
        for result in callback.result():
            results.extend(result)
        return results
    else:
        print(f"No results returned from query: {query}")


async def get_count():   
    res = submit("g.V().count()")
    return res


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
