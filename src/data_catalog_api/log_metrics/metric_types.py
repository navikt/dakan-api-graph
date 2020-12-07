from prometheus_client import Counter, Summary

# Node by id
GET_NODE_BY_ID_SUCCESS = Counter('data_catalog_api_counter_get_node_by_id_success',
                                 'Counter get node by id endpoint success')

GET_NODE_BY_ID_MULTIPLE_NODES_ERROR = Counter('data_catalog_api_counter_get_node_by_id_multiple_nodes',
                                              'Counter get node by id endpoint multiple nodes error')

GET_NODE_BY_ID_NOT_FOUND = Counter('data_catalog_api_counter_get_node_by_id_not_found',
                                   'Counter get node by id not found')

GET_NODE_BY_ID_CONNECTION_REFUSED = Counter('data_catalog_api_counter_get_node_by_id_connection_refused',
                                            'Counter get node by id connection refused')

REQUEST_TIME_GET_NODE_BY_ID = Summary('data_catalog_api_request_time_get_node_by_id',
                                      'Time spent processing get request')
# Nodes by label
GET_NODE_BY_LABEL_SUCCESS = Counter('data_catalog_api_counter_get_node_by_label_success',
                                    'Counter get node by label endpoint success')

GET_NODE_BY_LABEL_NOT_FOUND = Counter('data_catalog_api_counter_get_node_by_label_not_found',
                                      'Counter get node by label none found')

GET_NODE_BY_LABEL_CONNECTION_REFUSED = Counter('data_catalog_api_counter_get_node_by_label_connection_refused',
                                               'Counter get node by label connection refused')

REQUEST_TIME_GET_NODE_BY_LABEL = Summary('data_catalog_api_request_time_get_node_by_label',
                                         'Time spent processing get request')

# Nodes by outward relation
GET_NODES_BY_OUTWARD_RELATION_SUCCESS = Counter('data_catalog_api_counter_get_nodes_by_outward_relation_success',
                                                'Counter get nodes by outward relation endpoint success')

GET_NODES_BY_OUTWARD_RELATION_NOT_FOUND = Counter('data_catalog_api_counter_get_nodes_by_outward_relation_not_found',
                                                  'Counter get nodes by outward relation none found')

GET_NODES_BY_OUTWARD_RELATION_CONNECTION_REFUSED = Counter(
    'data_catalog_api_counter_get_nodes_by_outward_relation_connection_refused',
    'Counter get nodes by outward relation connection refused')

REQUESTS_TIME_GET_NODE_BY_OUTWARD_RELATION = Summary('data_catalog_api_request_time_get_nodes_by_outward_relation',
                                                     'Time spent processing get request')

# Nodes by inward relation
GET_NODES_BY_INWARD_RELATION_SUCCESS = Counter('data_catalog_api_counter_get_nodes_by_inward_relation_success',
                                               'Counter get nodes by inward relation endpoint success')

GET_NODES_BY_INWARD_RELATION_NOT_FOUND = Counter('data_catalog_api_counter_get_nodes_by_inward_relation_not_found',
                                                 'Counter get nodes by inward relation none found')

GET_NODES_BY_INWARD_RELATION_CONNECTION_REFUSED = Counter(
    'data_catalog_api_counter_get_nodes_by_inward_relation_connection_refused',
    'Counter get nodes by inward relation connection refused')

REQUESTS_TIME_GET_NODE_BY_INWARD_RELATION = Summary('data_catalog_api_request_time_get_nodes_by_inward_relation',
                                                    'Time spent processing get request')


#  Upsert Node And Create Edge
UPSERT_NODE_AND_CREATE_EDGE_SUCCESS = Counter('data_catalog_api_counter_upsert_node_and_create_edge_success',
                                              'Counter upsert node and edge endpoint success')

UPSERT_NODE_AND_CREATE_EDGE_FAILED = Counter('data_catalog_api_counter_upsert_node_and_create_edge_failed',
                                             'Counter upsert node and edge endpoint failed')

UPSERT_NODE_AND_CREATE_EDGE_CONNECTION_REFUSED = Counter(
    'data_catalog_api_counter_upsert_node_and_create_edge_refused',
    'Counter upsert node and create edge connection refused')

REQUESTS_TIME_UPSERT_NODE_AND_CREATE_EDGE = Summary('data_catalog_api_request_time_upsert_node_and_create_edge',
                                                    'Time spent processing upsert node and edge request')

# Upsert Nodes
UPSERT_NODES_SUCCESS = Counter('data_catalog_api_counter_upsert_nodes_success',
                               'Counter upsert nodes endpoint success')

UPSERT_NODES_FAILED = Counter('data_catalog_api_counter_upsert_nodes_failed',
                              'Counter upsert nodes endpoint failed')

UPSERT_NODES_CONNECTION_REFUSED = Counter('data_catalog_api_counter_upsert_nodes_connection_refused',
                                          'Counter upsert nodes connection refused')

REQUESTS_TIME_UPSERT_NODES = Summary('data_catalog_api_request_time_upsert_nodes',
                                     'Time spent processing upsert request')

# Delete Nodes
DELETE_NODES_SUCCESS = Counter('data_catalog_api_counter_delete_nodes_success',
                               'Counter delete nodes endpoint success')

DELETE_NODES_FAILED = Counter('data_catalog_api_counter_delete_nodes_failed',
                              'Counter delete nodes endpoint failed')

DELETE_NODES_CONNECTION_REFUSED = Counter('data_catalog_api_counter_delete_nodes_connection_refused',
                                          'Counter delete nodes connection refused')

REQUESTS_TIME_DELETE_NODES = Summary('data_catalog_api_request_time_delete_nodes',
                                     'Time spent processing delete request')

# Delete Nodes By Type
DELETE_NODES_BY_TYPE_SUCCESS = Counter('data_catalog_api_counter_delete_nodes_by_type_success',
                                       'Counter delete nodes by type endpoint success')

DELETE_NODES_BY_TYPE_FAILED = Counter('data_catalog_api_counter_delete_nodes_by_type_failed',
                                      'Counter delete nodes by type endpoint failed')

DELETE_NODES_BY_TYPE_CONNECTION_REFUSED = Counter('data_catalog_api_counter_delete_nodes_by_type_connection_refused',
                                                  'Counter delete nodes by type connection refused')

REQUESTS_TIME_DELETE_NODES_BY_TYPE = Summary('data_catalog_api_request_time_delete_nodes_by_type',
                                             'Time spent processing delete by type request')

# Invalidate Nodes By Type
INVALIDATE_NODES_SUCCESS = Counter('data_catalog_api_counter_invalidate_nodes_success',
                                   'Counter invalidate nodes endpoint success')

INVALIDATE_NODES_FAILED = Counter('data_catalog_api_counter_invalidate_nodes_failed',
                                  'Counter invalidate nodes endpoint failed')

INVALIDATE_NODES_CONNECTION_REFUSED = Counter('data_catalog_api_counter_invalidate_nodes_connection_refused',
                                              'Counter invalidate nodes connection refused')

REQUESTS_TIME_INVALIDATE_NODES = Summary('data_catalog_api_request_time_invalidate_nodes',
                                         'Time spent processing invalidate request')

# Edge by id
GET_EDGE_BY_ID_SUCCESS = Counter('data_catalog_api_counter_get_edge_by_id_success',
                                 'Counter get edge by id endpoint success')

GET_EDGE_BY_ID_MULTIPLE_EDGES_ERROR = Counter('data_catalog_api_counter_get_edge_by_id_multiple_nodes',
                                              'Counter get edge by id endpoint multiple nodes error')

GET_EDGE_BY_ID_NOT_FOUND = Counter('data_catalog_api_counter_get_edge_by_id_not_found',
                                   'Counter get edge by id not found')

GET_EDGE_BY_ID_CONNECTION_REFUSED = Counter('data_catalog_api_counter_get_edge_by_id_connection_refused',
                                            'Counter get edge by id connection refused')

REQUEST_TIME_GET_EDGE_BY_ID = Summary('data_catalog_api_request_time_get_edge_by_id',
                                      'Time spent processing get edge request')

# Get Edge by label
GET_EDGE_BY_LABEL_SUCCESS = Counter('data_catalog_api_counter_get_edge_by_label_success',
                                 'Counter get edge by label endpoint success')

GET_EDGE_BY_LABEL_NOT_FOUND = Counter('data_catalog_api_counter_get_edge_by_label_not_found',
                                   'Counter get edge by label not found')

GET_EDGE_BY_LABEL_CONNECTION_REFUSED = Counter('data_catalog_api_counter_get_edge_by_label_connection_refused',
                                            'Counter get edge by label connection refused')

REQUEST_TIME_GET_EDGE_BY_LABEL = Summary('data_catalog_api_request_time_get_edge_by_label',
                                      'Time spent processing get edge by label request')

# Upsert Edges
UPSERT_EDGES_SUCCESS = Counter('data_catalog_api_counter_upsert_edges_success',
                               'Counter upsert edges endpoint success')

UPSERT_EDGES_FAILED = Counter('data_catalog_api_counter_upsert_edges_failed',
                              'Counter upsert edges endpoint failed')

UPSERT_EDGES_CONNECTION_REFUSED = Counter('data_catalog_api_counter_upsert_edges_connection_refused',
                                          'Counter upsert edges connection refused')

REQUESTS_TIME_UPSERT_EDGES = Summary('data_catalog_api_request_time_upsert_edges',
                                     'Time spent processing upsert edge request')

# Delete Edges
DELETE_EDGES_SUCCESS = Counter('data_catalog_api_counter_delete_edges_success',
                               'Counter delete edges endpoint success')

DELETE_EDGES_FAILED = Counter('data_catalog_api_counter_delete_edges_failed',
                              'Counter delete edges endpoint failed')

DELETE_EDGES_CONNECTION_REFUSED = Counter('data_catalog_api_counter_delete_edges_connection_refused',
                                          'Counter delete edges connection refused')

REQUESTS_TIME_DELETE_EDGES = Summary('data_catalog_api_request_time_delete_edges',
                                     'Time spent processing delete edge request')

# Delete Edges by label
DELETE_EDGES_BY_LABEL_SUCCESS = Counter('data_catalog_api_counter_delete_edges_by_label_success',
                                        'Counter delete edges by label endpoint success')

DELETE_EDGES_BY_LABEL_FAILED = Counter('data_catalog_api_counter_delete_edges_by_label_failed',
                                       'Counter delete edges by label endpoint failed')

DELETE_EDGES_BY_LABEL_CONNECTION_REFUSED = Counter('data_catalog_api_counter_delete_edges_by_label_connection_refused',
                                                   'Counter delete edges by label connection refused')

REQUESTS_TIME_DELETE_EDGES_BY_LABEL = Summary('data_catalog_api_request_time_delete_edges_by_label',
                                              'Time spent processing delete edge by label request')

# Delete all edges of a node
DELETE_ALL_EDGES_OF_NODE_SUCCESS = Counter('data_catalog_api_counter_delete_all_edges_of_node_success',
                                           'Counter delete all edges of node success')

DELETE_ALL_EDGES_OF_NODE_FAILED = Counter('data_catalog_api_counter_delete_all_edges_of_node_failed',
                                          'Counter delete all edges of node failed')

DELETE_ALL_EDGES_OF_NODE_CONNECTION_REFUSED = Counter(
    'data_catalog_api_counter_delete_all_edges_of_node_connection_refused',
    'Counter delete all edges of node connection refused')

REQUESTS_TIME_DELETE_ALL_EDGES_OF_NODE = Summary(
    'data_catalog_api_request_time_delete_all_edges_of_node',
    'Time spent processing delete all edges of node')
