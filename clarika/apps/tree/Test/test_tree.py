
import unittest
from unittest.mock import patch

from clarika.apps.tree.config_global_var import NODE_LEVEL
from clarika.apps.tree.config_global_var import NODE_VALUE_SIZE
from clarika.apps.tree.exception import LengthNodeValueExceMax
from clarika.apps.tree.exception import NodeIdDoesNotExit
from clarika.apps.tree.exception import SizeNodeExceMax
from clarika.apps.tree.utility_tree import Node
from clarika.apps.tree.utility_tree import Tree
from clarika.apps.tree.utility_tree import UtilityNode


class TestNodeMethods(unittest.TestCase):

    def test_length_node_value(self):
        with self.assertRaises(LengthNodeValueExceMax):
            repeated_a = "a" * (NODE_VALUE_SIZE+1)
            node = Node()
            node.set_value(repeated_a)

    def test_set_id(self):
        node = Node()
        node.set_id(1)
        self.assertEqual(node.get_id(), 1)

    def test_delete_node_and_children(self):
        root = Node()
        child1 = Node(parent=root)
        child2 = Node(parent=child1)
        child1.children.append(child2)
        root.children.append(child1)

        root.delete_node_and_children()
        self.assertTrue(child1.get_deleted_value())
        self.assertTrue(child2.get_deleted_value())

    def test_restor_node_and_children(self):
        root = Node()
        child1 = Node(parent=root)
        child2 = Node(parent=child1)
        child1.children.append(child2)
        root.children.append(child1)

        root.delete_node_and_children()
        self.assertTrue(child1.get_deleted_value())
        self.assertTrue(child2.get_deleted_value())

        root.restor_node_and_children()
        self.assertFalse(child1.get_deleted_value())
        self.assertFalse(child2.get_deleted_value())

    def test_set_value(self):
        node = Node()
        node.set_value("TestValue")
        self.assertEqual(node.value, "TestValue")



class TestTreeMethods(unittest.TestCase):

    def test_add_node(self):
        root = Node()
        tree = Tree(root)
        child = Node()

        self.assertTrue(tree.add_node(child, root.get_id()))
        self.assertEqual(len(root.children), 1)


    def test_size_node_exced(self):
        with self.assertRaises(SizeNodeExceMax):
            node = Node()
            tree = Tree(node)
            for i in range(1,NODE_LEVEL+2):
                tree.add_node(Node(),i)

    def test_node_id_not_ex(self):
        node = Node()
        tree = Tree(node)
        self.assertIsNone( tree.find_node(tree.root,20))



    def test_delete_node(self):
        root = Node()
        tree = Tree(root)
        child = Node()

        tree.add_node(child, root.get_id())
        self.assertTrue(tree.delete_node_by_id(child.get_id()))
        self.assertTrue(child.get_deleted_value())

    def test_restore_node_and_children(self):
        root = Node()
        tree = Tree(root)
        child = Node()

        tree.add_node(child, root.get_id())
        child.delete_node_and_children()
        self.assertTrue(tree.restore_node_and_children(child.get_id()))
        self.assertFalse(child.get_deleted_value())

    def test_find_node(self):
        root = Node()
        tree = Tree(root)
        child = Node()
        tree.add_node(child, root.get_id())

        found_node = tree.find_node(root, child.get_id())
        self.assertEqual(found_node, child)

    def test_get_level_and_node(self):
        root = Node()
        tree = Tree(root)
        child1 = Node()
        child2 = Node()
        child1_child = Node()
        tree.add_node(child1, root.get_id())
        tree.add_node(child2, root.get_id())
        tree.add_node(child1_child, child1.get_id())

        node, level = tree.get_level_and_node(root, child2.get_id())
        self.assertEqual(node, child2)
        self.assertEqual(level, 1)

    def test_create_new_node(self):
        root = Node()
        tree = Tree(root)
        child = Node()
        tree.add_node(child, root.get_id())

        new_node = tree.create_new_node(child.get_id())
        self.assertIsNone(new_node.parent)
        self.assertFalse(child in root.children)

class TestUtilityNode(unittest.TestCase):
    def test_dict_to_node_no_child(self):
        data1 = {
                'value'   : 'SimpleNode',
                'node_id' : 1,
                'deleted' : False,
                'children': []
                }

        tree1 = Tree(Node())
        aux = UtilityNode()
        result_node1 = aux.dict_to_node(data1)

        self.assertEqual(result_node1.value, 'SimpleNode')
        self.assertEqual(result_node1.get_id(), 1)
        self.assertFalse(result_node1.get_deleted_value())
        self.assertFalse(result_node1.children)





    def test_dict_to_node_delete_1_child(self):
        data2 = {
                'value'   : 'RootNode',
                'node_id' : 1,
                'deleted' : False,
                'children': [
                        {
                                'value'   : 'ChildNode1',
                                'node_id' : 2,
                                'deleted' : True,
                                'children': []
                                },
                        {
                                'value'   : 'ChildNode2',
                                'node_id' : 3,
                                'deleted' : False,
                                'children': [
                                        {
                                                'value'   : 'GrandchildNode1',
                                                'node_id' : 4,
                                                'deleted' : False,
                                                'children': []
                                                }
                                        ]
                                }
                        ]
                }


        aux = UtilityNode()
        result_node2 = aux.dict_to_node(data2)

        self.assertEqual(result_node2.value, 'RootNode')
        self.assertEqual(result_node2.get_id(), 1)
        self.assertFalse(result_node2.get_deleted_value())
        self.assertTrue(result_node2.children)
        self.assertEqual(len(result_node2.children), 2)
        self.assertTrue(result_node2.children[0].value)
        self.assertTrue(result_node2.children[1].children)
        self.assertEqual(result_node2.children[1].children[0].value, 'GrandchildNode1')


if __name__ == '__main__':
    unittest.main()
