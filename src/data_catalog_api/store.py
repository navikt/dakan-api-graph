import logging
import os
import ast 
import json

from fastapi import HTTPException

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.process.traversal import T, P, Operator
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.io import graphsonV2d0
from gremlin_python.driver import client, serializer
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.driver.request import RequestMessage

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

from dotenv import load_dotenv
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
                       message_serializer=serializer.GraphSONSerializersV2d0()
                    )

def submit(query, message=None, params=None):
    callback = cosmosdb_conn.submitAsync(query)
    results = []
    if callback.result() is not None:
        for result in callback.result():
            results.extend(result)
        return results
    else:
        print(f"No results returned from query: {gremlinQuery}")


async def get_count():   
    res = submit("g.V().count()")
    return(res)


async def get_node_by_id(node_id: str):
    res = submit(f"g.V('{node_id}')")
    return(res)

async def get_node_by_label_id(label: str, node_id: str):
    res = submit(f"g.V.hasLabel('{label}').has('id', '{node_id}')")
    return(res)

async def upsert_node(label: str, id: str, content: str):
    query = f"g.V().hasLabel('{label}').has('id','{id}').fold().coalesce(unfold(),addV('{label}').property('id','{id}').property('version','1')"
    content_dict = ast.literal_eval(content)
    params = ""
    for key, value in content_dict.items():
        params = f"{params}.property('{key}','{value}')"
    
    print(content)
    print(query+params)

    res = submit(query+params + ')')
    return res

    #return(query)

async def add_property_to_node(node_id: str, property_key: str, property_val: str):
    query = f"g.V('{node_id}').property('{property_key}','{property_val}')"
    res = submit(query)
    return(res)

