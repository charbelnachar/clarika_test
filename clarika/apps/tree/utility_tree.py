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
        # if not self.deleted:
        print('  ' * indent + str(self.id) + ": " + self.value +": " + str(self.deleted))
        for child in self.children:
            child.print_tree(indent + 1)

    def to_dict(self)->dict:
        """
        Convierte el nodo y su estructura de árbol en un diccionario.

        :return: Diccionario que representa el nodo y su estructura de árbol.
        """
        return {
                'node_id' : self.id,
                'value'   : self.value,
                'deleted' : self.deleted,
                'children': [child.to_dict() for child in self.children]
                }

    def to_dict_no_deleted(self)-> dict:
        """
        Convierte el nodo y su estructura de árbol en un diccionario, excluyendo los nodos eliminados.

        :return: Diccionario que representa el nodo y su estructura de árbol, excluyendo los nodos eliminados.
        """
        return {
                'node_id' : self.id,
                'value'   : self.value,
                'deleted' : self.deleted,
                'children': [child.to_dict() for child in self.children if not child.deleted]
                }

    def delete_one_node(self)-> None:
        """
        Marca el nodo actual como eliminado.
        """
        self.deleted = True

    def has_children_not_deleted(self) -> bool:
        """
        Verifica si el nodo tiene hijos que no están marcados como eliminados.

        :return: True si el nodo tiene al menos un hijo no eliminado; False en caso contrario.
        """
        for child in self.children:
            if not child.deleted:
                return True
        return False

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
        if parent_node is not None :
            if level < NODE_LEVEL:
                if not parent_node.deleted:
                    self.count_id_node += 1
                    node.set_id(self.count_id_node)
                    node.parent = parent_node
                    parent_node.children.append(node)
                    return True
                else:
                    raise NodeIsDeleted(parent_id)
            else:
                raise SizeNodeExceMax(level)
        else:
            raise  NodeIdDoesNotExit(parent_id)



    def delete_node_by_id(self, node_id: int) -> bool:
        """
        Marca un nodo por id  y sus hijos como eliminados en el árbol.

        :param node_id: ID del nodo a eliminar.
        :return: True si el nodo se eliminó correctamente, False en caso contrario.
        """
        node = self.find_node(self.root, node_id)
        if node:
            node.delete_node_and_children()
            return True
        return False

    def delete_node_by_node(self, node: Node) -> bool:
        """
        Marca un nodo y sus hijos como eliminados en el árbol.

        :param node: nodo a eliminar.
        :return: True si el nodo se eliminó correctamente, False en caso contrario.
        """

        if node:
            node.delete_node_and_children()
            return True
        return False

    def delete_one_node(self, node_id: int) -> bool:
        """
        Marca un nodo como eliminados en el árbol.

        :param node_id: ID del nodo a eliminar.
        :return: True si el nodo se eliminó correctamente, False en caso contrario.
        """
        node = self.find_node(self.root, node_id)
        if node and not node.get_deleted_value():
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
        return (None,None)

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

    def adjust_ids(self, node, next_id) -> None:
        """
        Ajusta los ID de los nodos en el árbol y sus hijos al agregar un valor especificado a cada ID.

        :param node: Nodo al que se le ajustará el ID.
        :param next_id: Valor a agregar a cada ID.
        :return: None
        """
        node.id += next_id
        for child in node.children:
            self.adjust_ids(child, next_id)

        self.count_id_node += 1

    def get_depth(self, node)->int:
        """
        Obtiene la profundidad máxima del árbol a partir del nodo dado.

        :param node: Nodo desde el que se calculará la profundidad.
        :return: Profundidad máxima del árbol a partir del nodo dado.
        """
        if not node.children:
            return 1
        return 1 + max(self.get_depth(child) for child in node.children)

    def reset(self) -> None:
        self.count_id_node = 0
        current_nodes = [self.root]
        node_id = 1
        max_nodes = 10  # Número máximo de nodos
        max_levels = 4  # Número máximo de niveles

        while node_id <= max_nodes:
            next_level_nodes = []
            for current_node in current_nodes:
                for _ in range(max_nodes // len(current_nodes)):
                    if node_id > max_nodes:
                        break
                    new_node = Node(current_node.id)
                    new_node.set_value(f'Node {node_id}')
                    new_node.set_id(node_id)
                    current_node.children.append(new_node)
                    next_level_nodes.append(new_node)
                    node_id += 1
            current_nodes = next_level_nodes

        # Marcar como eliminados los nodos restantes
        for current_node in current_nodes:
            for child in current_node.children:
                child.delete_node_and_children()



    def add_subtree_by_id(self, new_subtree, node_id)->None:
        """
                Agrega un nuevo subárbol al nodo especificado por ID en el árbol actual.

                :param new_subtree: Nuevo subárbol a agregar.
                :param node_id: ID del nodo al que se agregará el nuevo subárbol.
                :raises: SizeNodeExceMax si la profundidad del árbol después de la adición excede NODE_LEVEL.
                :return: None
                """
        level_tree1 = self.get_depth(self.root)
        level_tree2 = self.get_depth(new_subtree.root)
        if self.get_depth(self.root) + self.get_depth(new_subtree.root) > NODE_LEVEL:
            raise SizeNodeExceMax(level_tree1 + level_tree2)

        self.adjust_ids(new_subtree.root, self.count_id_node)

        node = self.find_node(self.root, node_id)
        if node is not None:
            node.children.append(new_subtree.root)

    def add_subtree_by_node(self, new_subtree, node)->None:
        """
                Agrega un nuevo subárbol al nodo especificado por Nodo en el árbol actual.

                :param new_subtree: Nuevo subárbol a agregar.
                :param node_id: ID del nodo al que se agregará el nuevo subárbol.
                :raises: SizeNodeExceMax si la profundidad del árbol después de la adición excede NODE_LEVEL.
                :return: None
                """
        # Verificar que la adición del nuevo subárbol no haga que el árbol antiguo supere el límite de 10 niveles
        level_tree1 =  self.get_depth(self.root)
        level_tree2 = self.get_depth(new_subtree.root)
        if self.get_depth(self.root) + self.get_depth(new_subtree.root) > NODE_LEVEL:
            raise SizeNodeExceMax(level_tree1+level_tree2)


        # Ajustar los ID de los nodos del nuevo subárbol
        self.adjust_ids(new_subtree.root, self.count_id_node)

        # Agregar el nuevo subárbol al nodo especificado en el árbol antiguo
        if node is not None:
            node.children.append(new_subtree.root)

class UtilityNode:
    def dict_to_node(self,data) ->Node:
        """
               Convierte un diccionario de datos en un nodo y sus hijos.

               :param data: Diccionario de datos que representa un nodo y sus hijos.
               :return: El nodo generado a partir del diccionario.
               """
        node = Node()
        node.set_value(data['value'])
        node.set_id(data['node_id'])
        node.deleted = data['deleted']
        node.children = [self.dict_to_node(child_data) for child_data in data['children']]
        return node


