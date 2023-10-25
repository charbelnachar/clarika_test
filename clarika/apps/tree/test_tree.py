
import unittest
from unittest.mock import patch
from clarika.apps.tree.utility_tree  import Node, Tree

class TestNodeMethods(unittest.TestCase):

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


    def test_delete_node(self):
        root = Node()
        tree = Tree(root)
        child = Node()

        tree.add_node(child, root.get_id())
        self.assertTrue(tree.delete_node(child.get_id()))
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

if __name__ == '__main__':
    unittest.main()
