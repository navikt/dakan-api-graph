from prometheus_client import Counter, Summary

# Node by id
GET_NODE_BY_ID_SUCCESS = Counter('data_catalog_api_counter_get_node_by_id_success',
                                 'Counter get node by id endpoint success')

GET_NODE_BY_ID_MULTIPLE_NODES_ERROR = Counter('data_catalog_api_counter_get_node_by_id_multiple_nodes',
                                              'Counter get node by id endpoint multiple nodes error')

GET_NODE_BY_ID_NOT_FOUND = Counter('data_catalog_api_counter_get_node_by_id_not_found',
                                   'Counter get node by id endpoint success')

REQUEST_TIME_GET_NODE_BY_ID = Summary('data_catalog_api_request_time_get_node_by_id',
                                      'Time spent processing request')
# Nodes by label
GET_NODE_BY_LABEL_SUCCESS = Counter('data_catalog_api_counter_get_node_by_label_success',
                                    'Counter get node by label endpoint success')

GET_NODE_BY_LABEL_NOT_FOUND = Counter('data_catalog_api_counter_get_node_by_label_not_found',
                                      'Counter get node by label endpoint success')

REQUEST_TIME_GET_NODE_BY_LABEL = Summary('data_catalog_api_request_time_get_node_by_label',
                                         'Time spent processing request')

# Nodes by outward relation
GET_NODES_BY_OUTWARD_RELATION_SUCCESS = Counter('data_catalog_api_counter_get_nodes_by_outward_relation_success',
                                                'Counter get nodes by outward_relation endpoint success')

GET_NODES_BY_OUTWARD_RELATION_NOT_FOUND = Counter('data_catalog_api_counter_get_nodes_by_outward_relation_not_found',
                                                  'Counter get nodes by outward_relation endpoint success')

REQUESTS_TIME_GET_NODE_BY_OUTWARD_RELATION = Summary('data_catalog_api_request_time_get_nodes_by_outward_relation',
                                                     'Time spent processing request')

# Nodes by inward relation
GET_NODES_BY_INWARD_RELATION_SUCCESS = Counter('data_catalog_api_counter_get_nodes_by_inward_relation_success',
                                               'Counter get nodes by inward_relation endpoint success')

GET_NODES_BY_INWARD_RELATION_NOT_FOUND = Counter('data_catalog_api_counter_get_nodes_by_inward_relation_not_found',
                                                 'Counter get nodes by inward_relation endpoint success')

REQUESTS_TIME_GET_NODE_BY_INWARD_RELATION = Summary('data_catalog_api_request_time_get_nodes_by_inward_relation',
                                                    'Time spent processing request')
