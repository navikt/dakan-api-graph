from prometheus_client import Counter, Summary

GET_NODE_BY_ID = Counter('data_catalog_api_counter_get_node_by_id',
                         'Counter for internal server error when reading from ceph bucket storage')

# Prometheus timers
REQUEST_TIME_GET_NODE_BY_ID = Summary('data_catalog_api_request_time_get_node_by_id',
                                      'Time spent processing request')
