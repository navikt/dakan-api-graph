import logging
import os
import json
import requests
import math
from json import JSONDecodeError
from typing import List
from data_catalog_api.log_metrics import metric_types
from data_catalog_api.models.edges import Edge
from data_catalog_api.models.nodes import Node, NodeResponse
from data_catalog_api.models.requests import NodeRelationPayload
from data_catalog_api.utils.cosmos_connector import CosmosConnector
from data_catalog_api.utils.logger import Logger
from fastapi import status
from fastapi.responses import JSONResponse
from data_catalog_api.exceptions.exceptions import MultipleNodesInDbError
from datetime import datetime

logger = Logger()
cosmosdb_conn = CosmosConnector()


def transform_node_response(nodes: List[NodeResponse]):
    for node in nodes:
        for key, value in node["properties"].items():
            try:
                new_value = json.loads(value[0]["value"])
            except JSONDecodeError:
                dumped_text = json.dumps(value[0]["value"])
                new_value = json.loads(dumped_text)

            if type(new_value) == str or isinstance(new_value, str):
                new_value = new_value.replace('"', '')
                new_value = new_value.replace("*", "'")

            node["properties"][key] = new_value


def get_node_by_id(node_id: str):
    try:
        res = cosmosdb_conn.submit(f"g.V('{node_id}')")
    except ConnectionRefusedError:
        metric_types.GET_NODE_BY_ID_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_NODE_BY_ID_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    if len(res) > 1:
        metric_types.GET_NODE_BY_ID_MULTIPLE_NODES_ERROR.inc()
        raise MultipleNodesInDbError(node_id)
    else:
        transform_node_response(res)
        metric_types.GET_NODE_BY_ID_SUCCESS.inc()
        return res[0]


def get_nodes_by_label(label: str, skip: int, limit: int, valid_nodes: bool):
    try:
        query = f"g.V().hasLabel('{label}')"

        if limit is not None:
            query += f".range({skip}, {skip + limit})"

        if valid_nodes is True:
            query += ".has('valid', 'true')"

        res = cosmosdb_conn.submit(query)

    except ConnectionRefusedError as e:
        metric_types.GET_NODE_BY_LABEL_CONNECTION_REFUSED.inc()
        logging.error(f"{e}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_NODE_BY_LABEL_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    transform_node_response(res)
    metric_types.GET_NODE_BY_LABEL_SUCCESS.inc()
    return res


def upsert_node(nodes: List[Node]):

    today = datetime.now().isoformat()

    for node in nodes:
        query = "g"
        params = ""
        params_no_partition_key = ""

        if 'valid_from' not in node.properties.items():
            params = f"{params}.property('valid_from','{today}')"
            params_no_partition_key = f"{params_no_partition_key}.property('valid_from','{today}')"

        if 'valid_to' not in node.properties.items():
            params = f"{params}.property('valid_to','')"
            params_no_partition_key = f"{params_no_partition_key}.property('valid_to','')"

        if 'valid' not in node.properties.items():
            params = f"{params}.property('valid','true')"
            params_no_partition_key = f"{params_no_partition_key}.property('valid','true')"

        for key, value in node.properties.items():
            clean_value = json.dumps(value).replace("'", "*")
            params = f"{params}.property('{key}','{clean_value}')"
            if key != os.environ["partitionKey"]:
                params_no_partition_key = f"{params_no_partition_key}.property('{key}','{clean_value}')"

        query += f".V().has('label','{node.label}').has('id','{node.id}')" \
                 f".fold().coalesce(unfold(){params_no_partition_key}," \
                 f"addV('{node.label}').property('id','{node.id}'){params})"

        try:
            res = cosmosdb_conn.submit(query)
        except ConnectionRefusedError:
            metric_types.UPSERT_NODES_CONNECTION_REFUSED.inc()
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                content={"Error": "Connection refused"})

        if res is None:
            metric_types.UPSERT_NODES_FAILED.inc()
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to upsert nodes"})

    metric_types.UPSERT_NODES_SUCCESS.inc()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"Successfully upserted {len(nodes)} nodes"})


def upsert_node_and_create_edge(payload: NodeRelationPayload):
    node = payload.node_body
    params = ""
    params_no_partition_key = ""
    for key, value in node.properties.items():
        clean_value = json.dumps(value).replace("'", "*")
        params = f"{params}.property('{key}','{clean_value}')"
        if key != os.environ["partitionKey"]:
            params_no_partition_key = f"{params_no_partition_key}.property('{key}','{clean_value}')"

    query = f"g.V().has('label','{node.label}').has('id','{node.id}').fold()" \
            f".coalesce(unfold(){params_no_partition_key}," \
            f"addV('{node.label}').property('id','{node.id}'){params})" \
            f".V('{payload.source_id}').as('out').V('{node.id}')" \
            f".coalesce(__.inE('{payload.edge_label}').where(outV().as('out')), " \
            f"addE('{payload.edge_label}').from('out'))"

    try:
        res = cosmosdb_conn.submit(query)
    except ConnectionRefusedError:
        metric_types.UPSERT_NODE_AND_CREATE_EDGE_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.UPSERT_NODE_AND_CREATE_EDGE_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": 'Failed to upsert and create edge'})

    metric_types.UPSERT_NODE_AND_CREATE_EDGE_SUCCESS.inc()
    return res


def delete_node(node_id: str):
    query_delete_node = f"g.V('{node_id}').drop()"

    try:
        res = cosmosdb_conn.submit(query_delete_node)
    except ConnectionRefusedError:
        metric_types.DELETE_NODES_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.DELETE_NODES_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to delete node"})

    metric_types.DELETE_NODES_SUCCESS.inc()
    return res


def delete_node_by_type(node_type: str):
    query_delete_node_by_type = f"g.V().hasLabel('{node_type}').limit(10000).drop()"

    try:
        res = cosmosdb_conn.submit(query_delete_node_by_type)
    except ConnectionRefusedError:
        metric_types.DELETE_NODES_BY_TYPE_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.DELETE_NODES_BY_TYPE_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to delete node"})

    metric_types.DELETE_NODES_BY_TYPE_SUCCESS.inc()
    return res


def get_out_nodes(node_id: str, edge_label: str, skip: int, limit: int, valid_nodes: bool):
    try:
        query = f"g.V('{node_id}').out('{edge_label}')"

        if limit is not None:
            query += f".range({skip}, {skip + limit})"

        if valid_nodes:
            query += ".has('valid', 'true')"

        res = cosmosdb_conn.submit(query)

    except ConnectionRefusedError:
        metric_types.GET_NODES_BY_OUTWARD_RELATION_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_NODES_BY_OUTWARD_RELATION_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    transform_node_response(res)
    metric_types.GET_NODES_BY_OUTWARD_RELATION_SUCCESS.inc()
    return res


def get_in_nodes(node_id: str, edge_label: str, skip: int, limit: int, valid_nodes: bool):
    try:
        query = f"g.V('{node_id}').in('{edge_label}')"

        if limit is not None:
            query += f".range({skip}, {skip + limit})"

        if valid_nodes:
            query += ".has('valid', 'true')"

        res = cosmosdb_conn.submit(query)

    except ConnectionRefusedError:
        metric_types.GET_NODES_BY_INWARD_RELATION_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_NODES_BY_INWARD_RELATION_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    transform_node_response(res)
    metric_types.GET_NODES_BY_INWARD_RELATION_SUCCESS.inc()
    return res


def invalidate_nodes(node_ids: List[str]):
    today = datetime.now().isoformat()

    for node_id in node_ids:

        query = f"g.V('{node_id}').property('valid', 'false').property('valid_to', '{today}')"

        try:
            res = cosmosdb_conn.submit(query)
        except ConnectionRefusedError:
            metric_types.INVALIDATE_NODES_CONNECTION_REFUSED.inc()
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                content={"Error": "Connection refused"})

        if res is None:
            metric_types.INVALIDATE_NODES_FAILED.inc()
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to invalidate nodes"})

    metric_types.INVALIDATE_NODES_SUCCESS.inc()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"Successfully invalidated {len(node_ids)} nodes"})


def get_edge_by_id(edge_id: str):
    try:
        res = cosmosdb_conn.submit("g.E('{id}')")
    except ConnectionRefusedError:
        metric_types.GET_EDGE_BY_ID_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_EDGE_BY_ID_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    if len(res) > 1:
        metric_types.GET_EDGE_BY_ID_MULTIPLE_EDGES_ERROR.inc()
        raise MultipleNodesInDbError(edge_id)
    else:
        metric_types.GET_EDGE_BY_ID_SUCCESS.inc()
        return res[0]


def get_edge_by_label(edge_label: str):
    query = f"g.E().hasLabel('{edge_label}')"

    try:
        res = cosmosdb_conn.submit(query)
    except ConnectionRefusedError:
        metric_types.GET_EDGE_BY_LABEL_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        metric_types.GET_EDGE_BY_LABEL_NOT_FOUND.inc()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    else:
        metric_types.GET_EDGE_BY_LABEL_SUCCESS.inc()
        return res


def upsert_edge(edges: List[Edge]):
    for edge in edges:
        query = "g"
        properties = ""
        for key, value in edge.properties.items():
            if not isinstance(value, list):
                properties = f"{properties}.property('{key}','{value}')"
            else:
                properties = f"{properties}.property('{key}','{json.dumps(value)}')"

        query += f".V('{edge.outV}').as('out').V('{edge.inV}')" \
                 f".coalesce(__.inE('{edge.label}').where(outV().as('out')){properties}, " \
                 f"addE('{edge.label}').from('out'){properties})"

        try:
            res = cosmosdb_conn.submit(query)
        except ConnectionRefusedError:
            metric_types.UPSERT_EDGES_CONNECTION_REFUSED.inc()
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                content={"Error": "Connection refused"})

        if res is None:
            metric_types.UPSERT_EDGES_FAILED.inc()
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to upsert edges"})

    metric_types.UPSERT_EDGES_SUCCESS.inc()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": f"Successfully upserted {len(edges)} edges"})


def delete_edge(source_id: str, target_id: str):
    query = f"g.V('{source_id}').outE().where(inV().hasId('{target_id}')).drop()"
    try:
        res = cosmosdb_conn.submit(query)
    except ConnectionRefusedError:
        metric_types.DELETE_EDGES_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.DELETE_EDGES_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to delete edge"})

    metric_types.DELETE_EDGES_SUCCESS.inc()
    return res


def delete_edge_by_label(edge_label: str):
    query = f"g.E().hasLabel('{edge_label}').limit(10000).drop()"
    try:
        res = cosmosdb_conn.submit(query)
    except ConnectionRefusedError:
        metric_types.DELETE_EDGES_BY_LABEL_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.DELETE_EDGES_BY_LABEL_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to delete edge"})

    metric_types.DELETE_EDGES_BY_LABEL_SUCCESS.inc()
    return res


def delete_all_edges_of_node(node_id: str):
    query = f"g.V('{node_id}').bothE().drop()"
    try:
        res = cosmosdb_conn.submit(query)
    except ConnectionRefusedError:
        metric_types.DELETE_ALL_EDGES_OF_NODE_CONNECTION_REFUSED.inc()
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if res is None:
        metric_types.DELETE_ALL_EDGES_OF_NODE_FAILED.inc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Error": "Failed to delete edge"})

    metric_types.DELETE_ALL_EDGES_OF_NODE_SUCCESS.inc()
    return res


def set_azure_max_throughput(throughput):
    if not (throughput.mode == 'manual' or throughput.mode == 'automatic'):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": "Throughput mode must be either 'manual' or 'automatic'."})
    if throughput.value < 4000 and throughput.mode == 'automatic':
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": "Throughput cannot be lower than 4000 in automatic mode."})
    if throughput.value < 1000 and throughput.mode == 'manual':
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": "Throughput cannot be lower than 1000 in manual mode."})

    res = requests.post(os.environ["azure_throughput_api"],
                        params={'maxThroughput': throughput.value, "mode": throughput.mode},
                        headers={'x-functions-key': os.environ["azure_throughput_key"]})

    return json.loads(res.content)


def get_nodes_by_label_test(label: str, page: int, valid_nodes: bool):
    response = {
        "page": page,
        "total_pages": 0,
        "max_items_per_page": 500,
        "total_items": "",
        "data": ""
    }

    limit = 500
    skip = (page - 1) * limit

    try:
        query_count = f"g.V().hasLabel('{label}')"
        query = f"g.V().hasLabel('{label}').range({skip}, {skip + limit})"

        if valid_nodes is True:
            query_count += ".has('valid', 'true')"
            query += ".has('valid', 'true')"

        query_count += ".count()"
        total_nodes = cosmosdb_conn.submit(query_count)
        response["total_items"] = total_nodes[0]
        response["total_pages"] = math.ceil(response["total_items"] / 500)
        res = cosmosdb_conn.submit(query)

    except ConnectionRefusedError as e:
        logging.error(f"{e}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if response["total_items"] == 0:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    transform_node_response(res)
    response["data"] = res

    return response


def term_search(term_name: str, term_status: str):
    try:
        query = "g.V().hasLabel('begrep').has('valid', 'true')"

        if term_status.lower() == 'godkjent':
            query += ".has('term_status', 'Godkjent begrep')"

        query += f".has('lowercase_term', TextP.containing('{term_name}')).or().has('lowercase_clean_definisjon', " \
                 f"TextP.containing('{term_name}'))"

        res = cosmosdb_conn.submit(query)

    except ConnectionRefusedError as e:
        logging.error(f"{e}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"Error": "Connection refused"})

    if len(res) == 0:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    transform_node_response(res)

    for term in res:
        term.update({'term': term['properties']['term']})
        term.update({'description': term['properties']['clean_definisjon']})
        term.update({'status': term['properties']['status']})

    return res
