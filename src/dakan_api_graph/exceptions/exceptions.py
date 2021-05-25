class MultipleNodesInDbError(Exception):

    def __init__(self, node_id):
        self.node_id = node_id

    def __str__(self):
        return f"""Multiple nodes with node id {self.node_id}"""


class EnvironmentVariableNotSet(Exception):

    def __init__(self, env_name):
        self.env_name = env_name

    def __str__(self):
        return f"""Required environment variable not set: {self.env_name}"""
