class MultipleNodesInDbError(Exception):

    def __init__(self, node_id):
        self.node_id = node_id

    def __str__(self):
        return f"""Multiple nodes with node id {self.node_id}"""
