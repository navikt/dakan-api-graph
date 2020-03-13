from prometheus_client import Counter, Summary

GET_NODE_BY_ID_SUCCESS = Counter('data_catalog_api_counter_get_node_by_id_success',
                                 'Counter get node by id endpoint success')

GET_NODE_BY_ID_MULTIPLE_NODES_ERROR = Counter('data_catalog_api_counter_get_node_by_id_multiple_nodes',
                                              'Counter get node by id endpoint multiple nodes error')

GET_NODE_BY_ID_NOT_FOUND = Counter('data_catalog_api_counter_get_node_by_id_not_found',
                                   'Counter get node by id endpoint success')


# Prometheus timers
REQUEST_TIME_GET_NODE_BY_ID = Summary('data_catalog_api_request_time_get_node_by_id',
                                      'Time spent processing request')
