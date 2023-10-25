from clarika.apps.tree.config_global_var import NODE_LEVEL
from clarika.apps.tree.config_global_var import NODE_VALUE_SIZE
from clarika.apps.tree.exception import LengthNodeValueExceMax
from clarika.apps.tree.exception import NodeIdDoesNotExit
from clarika.apps.tree.exception import NodeIsDeleted
from clarika.apps.tree.exception import SizeNodeExceMax


class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.deleted = False
        self.id = 0

    def set_id(self, node_id):
        self.id = node_id

    def get_id(self):
        return self.id

    def delete_node_and_children(self):
        self.deleted = True
        for child in self.children:
            child.delete_node_and_children()

    def restor_node_and_children(self):
        self.deleted = False
        for child in self.children:
            child.restor_node_and_children()

    def unmark_node_deleted(self):
        self.deleted = False

    def get_deleted_value(self):
        return self.deleted

    def set_value(self, value):
        if len(value) <= NODE_VALUE_SIZE:
            self.value = value
        else:
            raise LengthNodeValueExceMax(value)

    def print_tree(self, indent=0):
        if not self.deleted:
            print('  ' * indent + str(self.id) + ": " + self.value)
        for child in self.children:
            child.print_tree(indent + 1)


class Tree:
    count_id_node = 0

    def __init__(self, node):
        self.count_id_node += 1
        node.set_id(self.count_id_node)
        self.root = node

    def add_node(self, node, parent_id):
        parent_node, level = self.get_level_and_node(self.root, parent_id)
        if level < NODE_LEVEL:
            if parent_node:
                if not parent_node.deleted:
                    self.count_id_node += 1
                    node.set_id(self.count_id_node)
                    node.parent = parent_node
                    parent_node.children.append(node)
                    return True
                else:
                    raise NodeIsDeleted(parent_node)
            else:
                raise NodeIdDoesNotExit(parent_id)
        else:
            raise SizeNodeExceMax(level)

    def set_value(self, old_value, new_value):
        node = self.find_node(self.root, old_value)
        if node and not node.deleted:
            node.value = new_value
            return True
        return False

    def delete_node(self, node_id):
        node = self.find_node(self.root, node_id)
        if node and not node.get_deleted_value():
            node.delete_node_and_children()
            return True
        return False

    def restore_node_and_children(self, node_id):
        node = self.find_node(self.root, node_id)
        if node:
            node.restor_node_and_children()
            return True
        return False

    def find_node(self, start_node, node_id):
        if start_node.id == node_id:
            return start_node
        for child in start_node.children:
            result = self.find_node(child, node_id)
            if result:
                return result
        return None

    def get_level_and_node(self, start_node, node_id, current_level=0):

        if start_node.id == node_id:
            return start_node, current_level
        for child in start_node.children:
            result = self.get_level_and_node(child, node_id, current_level + 1)
            if result:
                node, level = result
                return (node, level)
        return None

    def create_new_node(self,node_id):
        node = self.find_node(self.root,node_id)
        # node = Node()
        node.parent.children.remove(node)
        node.parent = None
        return node