class LengthNodeValueExceMax(Exception):
    def __init__(self, value):
        self.value = value
        self.leng = len(value)


class SizeNodeExceMax(Exception):
    def __init__(self, value):
        self.value = value


class NodeIdDoesNotExit(Exception):
    def __init__(self, node_id):
        self.node_id = node_id

class NodeIsDeleted(Exception):
    def __init__(self, node_id):
        self.node_id = node_id
