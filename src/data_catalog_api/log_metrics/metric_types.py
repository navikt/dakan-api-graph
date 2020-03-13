from prometheus_client import Counter, Summary

# Node by id
GET_NODE_BY_ID_SUCCESS = Counter('data_catalog_api_counter_get_node_by_id_success',
                                 'Counter get node by id endpoint success')

GET_NODE_BY_ID_MULTIPLE_NODES_ERROR = Counter('data_catalog_api_counter_get_node_by_id_multiple_nodes',
                                              'Counter get node by id endpoint multiple nodes error')

GET_NODE_BY_ID_NOT_FOUND = Counter('data_catalog_api_counter_get_node_by_id_not_found',
                                   'Counter get node by id not found')

REQUEST_TIME_GET_NODE_BY_ID = Summary('data_catalog_api_request_time_get_node_by_id',
                                      'Time spent processing get request')
# Nodes by label
GET_NODE_BY_LABEL_SUCCESS = Counter('data_catalog_api_counter_get_node_by_label_success',
                                    'Counter get node by label endpoint success')

GET_NODE_BY_LABEL_NOT_FOUND = Counter('data_catalog_api_counter_get_node_by_label_not_found',
                                      'Counter get node by label none found')

REQUEST_TIME_GET_NODE_BY_LABEL = Summary('data_catalog_api_request_time_get_node_by_label',
                                         'Time spent processing get request')

# Nodes by outward relation
GET_NODES_BY_OUTWARD_RELATION_SUCCESS = Counter('data_catalog_api_counter_get_nodes_by_outward_relation_success',
                                                'Counter get nodes by outward relation endpoint success')

GET_NODES_BY_OUTWARD_RELATION_NOT_FOUND = Counter('data_catalog_api_counter_get_nodes_by_outward_relation_not_found',
                                                  'Counter get nodes by outward relation none found')

REQUESTS_TIME_GET_NODE_BY_OUTWARD_RELATION = Summary('data_catalog_api_request_time_get_nodes_by_outward_relation',
                                                     'Time spent processing get request')

# Nodes by inward relation
GET_NODES_BY_INWARD_RELATION_SUCCESS = Counter('data_catalog_api_counter_get_nodes_by_inward_relation_success',
                                               'Counter get nodes by inward relation endpoint success')

GET_NODES_BY_INWARD_RELATION_NOT_FOUND = Counter('data_catalog_api_counter_get_nodes_by_inward_relation_not_found',
                                                 'Counter get nodes by inward relation none found')

REQUESTS_TIME_GET_NODE_BY_INWARD_RELATION = Summary('data_catalog_api_request_time_get_nodes_by_inward_relation',
                                                    'Time spent processing get request')

#  Upsert Node And Create Edge
UPSERT_NODE_AND_CREATE_EDGE_SUCCESS = Counter('data_catalog_api_counter_upsert_node_and_create_edge_success',
                                              'Counter upsert node and edge endpoint success')

UPSERT_NODE_AND_CREATE_EDGE_FAILED = Counter('data_catalog_api_counter_upsert_node_and_create_edge_failed',
                                             'Counter upsert node and edge endpoint failed')

REQUESTS_TIME_UPSERT_NODE_AND_CREATE_EDGE = Summary('data_catalog_api_request_time_upsert_node_and_create_edge',
                                                    'Time spent processing upsert node and edge request')

# Upsert Nodes
UPSERT_NODES_SUCCESS = Counter('data_catalog_api_counter_upsert_nodes_success',
                               'Counter upsert nodes endpoint success')

UPSERT_NODES_FAILED = Counter('data_catalog_api_counter_upsert_nodes_failed',
                              'Counter upsert nodes endpoint failed')

REQUESTS_TIME_UPSERT_NODES = Summary('data_catalog_api_request_time_upsert_nodes',
                                     'Time spent processing upsert request')

# Delete Nodes
DELETE_NODES_SUCCESS = Counter('data_catalog_api_counter_delete_node_success',
                               'Counter delete nodes endpoint success')

DELETE_NODES_FAILED = Counter('data_catalog_api_counter_delete_nodes_failed',
                              'Counter delete nodes endpoint failed')

REQUESTS_TIME_DELETE_NODES = Summary('data_catalog_api_request_time_delete_nodes',
                                     'Time spent processing delete request')
