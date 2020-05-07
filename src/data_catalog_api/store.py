import logging
import os
from typing import List

from data_catalog_api.log_metrics import metric_types
from data_catalog_api.models.edges import Edge
from data_catalog_api.models.nodes import Node
from data_catalog_api.models.requests import NodeRelationPayload
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
    try:
        res = submit(f"g.V('{node_id}')")
    except ConnectionRefusedError:
        metric_types.GET_NODE_BY_ID_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_NODE_BY_ID_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    if len(res) > 1:
        metric_types.GET_NODE_BY_ID_MULTIPLE_NODES_ERROR.inc()
        raise MultipleNodesInDbError(node_id)
    else:
        metric_types.GET_NODE_BY_ID_SUCCESS.inc()
        return res[0]


async def get_nodes_by_label(label: str, skip: int, limit: int):
    try:
        if limit is None:
            res = submit(f"g.V().hasLabel('{label}')")
        else:
            res = submit(f"g.V().hasLabel('{label}').range({skip}, {skip+limit})")
    except ConnectionRefusedError as e:
        metric_types.GET_NODE_BY_LABEL_CONNECTION_REFUSED.inc()
        logging.error(f"{e}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_NODE_BY_LABEL_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    metric_types.GET_NODE_BY_LABEL_SUCCESS.inc()
    return res


async def upsert_node(nodes: List[Node]):
    for node in nodes:
        query = "g"
        params = ""
        params_no_partition_key = ""
        for key, value in node.properties.items():
            params = f"{params}.property('{key}','{value}')"
            if key != os.environ["partitionKey"]:
                params_no_partition_key = f"{params_no_partition_key}.property('{key}','{value}')"

        query += f".V().has('label','{node.label}').has('id','{node.id}')" \
                 f".fold().coalesce(unfold(){params_no_partition_key}," \
                 f"addV('{node.label}').property('id','{node.id}'){params})"
        try:
            res = submit(query)
        except ConnectionRefusedError:
            metric_types.UPSERT_NODES_CONNECTION_REFUSED.inc()
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

        if res is None:
            metric_types.UPSERT_NODES_FAILED.inc()
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Failed to upsert nodes"})

    metric_types.UPSERT_NODES_SUCCESS.inc()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"Successfully upserted {len(nodes)} nodes"})


async def upsert_node_and_create_edge(payload: NodeRelationPayload):
    node = payload.node_body
    params = ""
    for key, value in node.properties.items():
        params = f"{params}.property('{key}','{value}')"

    query = f"g.V().has('label','{node.label}').has('id','{node.id}').fold().coalesce(unfold(){params}," \
            f"addV('{node.label}').property('id','{node.id}').property('version','1'){params})" \
            f".V('{payload.source_id}').addE('{payload.edge_label}').to(g.V('{node.id}'))"
    try:
        res = submit(query)
    except ConnectionRefusedError:
        metric_types.UPSERT_NODE_AND_CREATE_EDGE_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.UPSERT_NODE_AND_CREATE_EDGE_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'Failed to upsert and create edge'})

    metric_types.UPSERT_NODE_AND_CREATE_EDGE_SUCCESS.inc()
    return res


async def delete_node(node_id: str):
    query_delete_node = f"g.V('{node_id}').drop()"

    try:
        res = submit(query_delete_node)
    except ConnectionRefusedError:
        metric_types.DELETE_NODES_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.DELETE_NODES_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Failed to delete node"})

    metric_types.DELETE_NODES_SUCCESS.inc()
    return res


async def get_out_nodes(node_id: str, edge_label: str):

    try:
        res = submit(f"g.V('{node_id}').out('{edge_label}')")
    except ConnectionRefusedError:
        metric_types.GET_NODES_BY_OUTWARD_RELATION_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_NODES_BY_OUTWARD_RELATION_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    metric_types.GET_NODES_BY_OUTWARD_RELATION_SUCCESS.inc()
    return res


async def get_in_nodes(node_id: str, edge_label: str):

    try:
        res = submit(f"g.V('{node_id}').in('{edge_label}')")
    except ConnectionRefusedError:
        metric_types.GET_NODES_BY_INWARD_RELATION_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_NODES_BY_INWARD_RELATION_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    metric_types.GET_NODES_BY_INWARD_RELATION_SUCCESS.inc()
    return res


async def get_edge_by_id(edge_id: str):

    try:
        res = submit("g.E('{id}')")
    except ConnectionRefusedError:
        metric_types.GET_EDGE_BY_ID_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_EDGE_BY_ID_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    if len(res) > 1:
        metric_types.GET_EDGE_BY_ID_MULTIPLE_EDGES_ERROR.inc()
        raise MultipleNodesInDbError(edge_id)
    else:
        metric_types.GET_EDGE_BY_ID_SUCCESS.inc()
        return res[0]


async def create_edge(edges: List[Edge]):
    for edge in edges:
        query = f"g.V('{edge.inV}').addE('{edge.label}').to(g.V('{edge.outV}'))"

        try:
            res = submit(query)
        except ConnectionRefusedError:
            metric_types.UPSERT_EDGES_CONNECTION_REFUSED.inc()
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

        if res is None:
            metric_types.UPSERT_EDGES_FAILED.inc()
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to upsert edges"})

    metric_types.UPSERT_EDGES_SUCCESS.inc()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"Successfully upserted {len(edges)} edges"})


async def delete_edge(source_id: str, target_id: str):
    query = f"g.V('{source_id}').outE().where(inV().hasId('{target_id}')).drop()"
    try:
        res = submit(query)
    except ConnectionRefusedError:
        metric_types.DELETE_EDGES_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.DELETE_EDGES_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Failed to delete edge"})

    metric_types.DELETE_EDGES_SUCCESS.inc()
    return res
