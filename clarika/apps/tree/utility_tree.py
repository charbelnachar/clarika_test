from clarika.apps.tree.config_global_var import NODE_LEVEL
from clarika.apps.tree.config_global_var import NODE_VALUE_SIZE
from clarika.apps.tree.exception import LengthNodeValueExceMax
from clarika.apps.tree.exception import NodeIdDoesNotExit
from clarika.apps.tree.exception import NodeIsDeleted
from clarika.apps.tree.exception import SizeNodeExceMax


class Node:
    def __init__(self, parent=None):
        """
        Inicializa un nodo en el árbol.

        :param parent: Nodo padre (default: None).
        """
        self.parent = parent
        self.children = []
        self.deleted = False
        self.id = 0

    def set_id(self, node_id) -> None:
        """
        Establece el ID del nodo.

        :param node_id: ID del nodo.
        """
        self.id = node_id

    def get_id(self) -> int:
        """
        Obtiene el ID del nodo.

        :return: ID del nodo.
        """
        return self.id

    def delete_node_and_children(self) -> None:
        """
        Marca el nodo y sus hijos como eliminados.
        """
        self.deleted = True
        for child in self.children:
            child.delete_node_and_children()

    def restor_node_and_children(self) -> None:
        """
        Restaura el nodo y sus hijos eliminados.
        """
        self.deleted = False
        for child in self.children:
            child.restor_node_and_children()

    def unmark_node_deleted(self) -> None:
        """
        Desmarca el nodo como eliminado.
        """
        self.deleted = False

    def get_deleted_value(self) -> bool:
        """
        Obtiene el estado de eliminación del nodo.

        :return: True si el nodo está eliminado, False en caso contrario.
        """
        return self.deleted

    def set_value(self, value: str) -> None:
        """
        Establece el valor del nodo.

        :param value: Valor del nodo.
        :raises: LengthNodeValueExceMax si el valor excede NODE_VALUE_SIZE.
        """
        if len(value) <= NODE_VALUE_SIZE:
            self.value = value
        else:
            raise LengthNodeValueExceMax(value)

    def print_tree(self, indent: int = 0) -> None:
        """
        Imprime el árbol recursivamente.

        :param indent: Nivel de sangría (default: 0).
        """
        if not self.deleted:
            print('  ' * indent + str(self.id) + ": " + self.value)
        for child in self.children:
            child.print_tree(indent + 1)


class Tree:
    count_id_node = 0

    def __init__(self, node: Node) -> None:
        """
        Inicializa un árbol con un nodo raíz.

        :param node: Nodo raíz del árbol.
        """
        self.count_id_node += 1
        node.set_id(self.count_id_node)
        self.root = node

    def add_node(self, node: Node, parent_id: int) -> bool:
        """
        Agrega un nodo al árbol como hijo del nodo con el ID especificado.

        :param node: Nodo a agregar.
        :param parent_id: ID del nodo padre.
        :return: True si el nodo se agregó correctamente, False en caso contrario.
        :raises: NodeIdDoesNotExit si el nodo padre no existe.
                 NodeIsDeleted si el nodo padre está marcado como eliminado.
                 SizeNodeExceMax si se excede el límite de tamaño del nodo.
        """
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



    def delete_node(self, node_id: int) -> bool:
        """
        Marca un nodo y sus hijos como eliminados en el árbol.

        :param node_id: ID del nodo a eliminar.
        :return: True si el nodo se eliminó correctamente, False en caso contrario.
        """
        node = self.find_node(self.root, node_id)
        if node and not node.get_deleted_value():
            node.delete_node_and_children()
            return True
        return False

    def restore_node_and_children(self, node_id: int) -> bool:
        """
        Restaura un nodo y sus hijos marcados como eliminados en el árbol.

        :param node_id: ID del nodo a restaurar.
        :return: True si el nodo se restauró correctamente, False en caso contrario.
        """
        node = self.find_node(self.root, node_id)
        if node:
            node.restor_node_and_children()
            return True
        return False

    def find_node(self, start_node: Node, node_id: int) -> Node:
        """
        Busca un nodo con el ID especificado en el árbol de forma recursiva.

        :param start_node: Nodo a partir del cual iniciar la búsqueda.
        :param node_id: ID del nodo a buscar.
        :return: El nodo con el ID especificado o None si no se encuentra.
        """
        if start_node.id == node_id:
            return start_node
        for child in start_node.children:
            result = self.find_node(child, node_id)
            if result:
                return result
        return None

    def get_level_and_node(self, start_node: Node, node_id: int, current_level: int = 0) -> (Node, int):
        """
        Obtiene el nivel y el nodo con el ID especificado en el árbol de forma recursiva.

        :param start_node: Nodo a partir del cual iniciar la búsqueda.
        :param node_id: ID del nodo a buscar.
        :param current_level: Nivel actual (default: 0).
        :return: Tupla (nodo, nivel) si se encuentra, None en caso contrario.
        """
        if start_node.id == node_id:
            return start_node, current_level
        for child in start_node.children:
            result = self.get_level_and_node(child, node_id, current_level + 1)
            if result:
                node, level = result
                return (node, level)
        return None

    def create_new_node(self, node_id: int) -> Node:
        """
        Crea un nuevo nodo a partir de uno existente en el árbol.

        :param node_id: ID del nodo existente a partir del cual crear el nuevo nodo.
        :return: El nodo creado a partir del nodo existente.
        """
        node = self.find_node(self.root, node_id)
        node.parent.children.remove(node)
        node.parent = None
        return node
