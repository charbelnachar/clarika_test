from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST

from clarika.apps.tree.config_global_var import NODE_LEVEL
from clarika.apps.tree.config_global_var import NODE_VALUE_SIZE
from clarika.apps.tree.exception import LengthNodeValueExceMax
from clarika.apps.tree.exception import NodeIdDoesNotExit
from clarika.apps.tree.exception import NodeIsDeleted
from clarika.apps.tree.exception import SizeNodeExceMax
from clarika.apps.tree.utility_tree import Node
from clarika.apps.tree.utility_tree import Tree
from clarika.apps.tree.utility_tree import UtilityNode

# list_tree = []
root_node = Node()
root_node.set_value("root")
tree = Tree(root_node)



class SaludoView(View):
    def put(self, request):
        tree2 = {
    "node_id": 1,
    "value": "root",
    "children": [
        {
            "node_id": 2,
            "value": "child 1",
            "children": [],
            "deleted": False
        },
        {
            "node_id": 3,
            "value": "child 2",
            "children": [
                {
                    "node_id": 4,
                    "value": "grandchild 1",
                    "children": [],
                    "deleted": False
                }
            ],
            "deleted": False
        }
    ],
    "deleted": False
}

        aux = UtilityNode()
        awae = aux.dict_to_node(tree2)
        tree3 = Tree(awae)
        node1 = Node()
        node1.set_value("node1")

        node2 = Node()
        node2.set_value("node2")

        node3 = Node()
        node3.set_value("node3")

        node4 = Node()
        node4.set_value("ode4")

        node5 = Node()
        node5.set_value("node5")
        node6 = Node()
        node6.set_value("node6")

        node7 = Node()
        node7.set_value("node7")

        tree = Tree(node1)

        tree.add_node(node2, 1)

        tree.add_node(node3, 2)

        tree.add_node(node4, 3)

        tree.add_node(node5, 4)

        tree.add_node(node6, 5)

        tree.add_node(node7, 6)

        # tree.add_node(node7, 3)
        a = tree.root
        a.print_tree()

        # tree.delete_node_by_id(4)
        # tree.add_node(node7,5)
        print()
        tree.root.print_tree()
        print("-----------------------")
        # tree.restore_node_and_children(2)
        print()
        a.print_tree()
        print("----------antes------------")
        # z = tree.create_new_node(5)
        # tree2 = Tree(z)
        # z.print_tree()
        # # tree2.restore_node_and_children(4)
        # print("--------despues-----------")
        # z.print_tree()
        print("--------viejo-----------")
        a.print_tree()
        # print("--------reset-----------")
        # tree.reset()
        tree.root.print_tree()
        tree.add_subtree_by_id(tree3,4)
        tree.add_subtree_by_id(tree3, 6)

        tree.reset()
        wa = tree.root.to_dict()
        return JsonResponse(wa)


# class CreateTreeView(View):
#     def post(self, request):
#         root_value = request.data.get("root_value", "root")
#         try:
#             node = Node()
#             node.set_value(root_value)
#             tree = Tree()
#             tree.add_node(node)
#         except LengthNodeValueExceMax as error:
#             return JsonResponse({"error": f'{error.value} excede el rango permitido de {NODE_VALUE_SIZE}'},
#                             status=HTTP_400_BAD_REQUEST)
#
#         return JsonResponse({"root_id": tree.root.id}, status=HTTP_200_OK)


class AddNodeTreeView(View):
    def post(self, request):
        data = JSONParser().parse(request)
        node_value = data.get("node_value", "")
        try:
            parent_id = int(data.get("parent_id", 0))
        except ValueError as e:
            return JsonResponse({"error": f'valor del id del padre no es un int'},
                            status=HTTP_400_BAD_REQUEST)
        try:
            node = Node()
            node.set_value(node_value)
            tree.add_node(node, parent_id)

        except LengthNodeValueExceMax as error:
            return JsonResponse({"error": f'{error.value} excede el rango permitido de {NODE_VALUE_SIZE}'},
                            status=HTTP_400_BAD_REQUEST)

        except SizeNodeExceMax as error:
            return JsonResponse({"error": f'El nivel del arbol excede el rango permitido de {NODE_LEVEL}'},
                            status=HTTP_400_BAD_REQUEST)

        except NodeIdDoesNotExit as error:
            return JsonResponse({"error": f'El id {error.node_id} no pertenece a ningun padre '},
                            status=HTTP_400_BAD_REQUEST)

        except NodeIsDeleted as error:
            return JsonResponse({"error": f'El nodo con ID:{error.node_id} ha sido eliminado '},
                            status=HTTP_400_BAD_REQUEST)

        return JsonResponse({"node_id": node.id}, status=HTTP_200_OK)

class EditValueNodeView(View):
    def put(self, request):
        node_value = request.data.get("node_value", "")
        try:
            node_id = int(request.data.get("node_id", 0))
        except ValueError as e:
            return JsonResponse({"error": f'valor del id del padre no es un int'},
                            status=HTTP_400_BAD_REQUEST)

        try:
            node = tree.find_node(tree.root, node_id)
            if node is not None:
                try:
                    node.set_value(node_value)

                except LengthNodeValueExceMax as error:
                    return JsonResponse({"error": f'{error.value} excede el rango permitido de {NODE_VALUE_SIZE}'},
                                    status=HTTP_400_BAD_REQUEST)

            else:
                return JsonResponse({"error": f'El id {node_id} no pertenece a ningun nodo '},
                                status=HTTP_400_BAD_REQUEST)

        except LengthNodeValueExceMax as error:
            return JsonResponse({"error": f'{error.value} excede el rango permitido de {NODE_VALUE_SIZE}'},
                            status=HTTP_400_BAD_REQUEST)

        return JsonResponse({"success": f'El id: {node_id} fue modificado'},
                        status=HTTP_200_OK)


class DeletedNodeView(View):
    def delete(self, request):
        data = JSONParser().parse(request)
        try:
            node_id = int(data.get("node_id", -1))
        except ValueError as e:
            return JsonResponse({"error": f'valor del id del padre no es un int'},
                            status=HTTP_400_BAD_REQUEST)

        flag_children = data.get("flag_children", True)

        node = tree.find_node(root_node, node_id)
        if node is not None:
            if flag_children:
                tree.delete_node_by_node(node)
            else:
                if not node.has_children_not_deleted():
                    node.delete_one_node()
                else:
                    return JsonResponse({"error": f'El id {node_id} tiene hijos sin eliminar'},
                                    status=HTTP_400_BAD_REQUEST)

        else:
            return JsonResponse({"error": f'El id {node_id} no pertenece a ningun nodo'},
                            status=HTTP_400_BAD_REQUEST)


        return JsonResponse({"success": f'El id: {node_id} fue eliminado'},
                            status=HTTP_200_OK)



class RestoreNodeView(View):
    def put(self,request):
        data = JSONParser().parse(request)
        try:
            node_id = int(data.get("node_id", -1))
        except ValueError as e:
            return JsonResponse({"error": f'valor del id del padre no es un int'},
                            status=HTTP_400_BAD_REQUEST)

        flag_children = data.get("flag_children", False)

        node = tree.find_node(root_node, node_id)
        if node is not None:
            if flag_children:
                tree.restore_node_and_children(node)
            else:
                node.unmark_node_deleted()

        else:
            return JsonResponse({"error": f'El id {node_id} no pertenece a ningun nodo'},
                            status=HTTP_400_BAD_REQUEST)


        return JsonResponse({"success": f'El id: {node_id} fue restuarado'},
                            status=HTTP_200_OK)

class GetNodeStructView(View):
    def get(self,request):

        flag_deleted = request.GET.get('flag_deleted',True)
        try:
            node_id = int(request.GET.get("node_id", -1))
        except ValueError as e:
            return JsonResponse({"error": f' El id no es un int'},
                            status=HTTP_400_BAD_REQUEST)

        node = tree.find_node(root_node, node_id)
        if node is not None:
            if flag_deleted:
                data_out = node.to_dict()
            else:
                data_out = node.to_dict_no_deleted()

        else:
            return JsonResponse({"error": f'El id {node_id} no pertenece a ningun nodo'},
                            status=HTTP_400_BAD_REQUEST)

        return JsonResponse({"data_out": data_out},
                        status=HTTP_200_OK)

class NewSubtreeSpecificNodeView(View):
    def put(self, request):
        data = JSONParser().parse(request)

        try:
            node_id = int(data.get("node_id", -1))
        except ValueError as e:
            return JsonResponse({"error": f' El id no es un int'},
                            status=HTTP_400_BAD_REQUEST)
        aux_subtree = data.get("subtree", None)
        aux_utility_node = UtilityNode()
        sub_tree = Tree(aux_utility_node.dict_to_node(aux_subtree))

        node = tree.find_node(tree.root, node_id)
        if node is not None:
            try:
                tree.add_subtree_by_node(sub_tree,node)
            except SizeNodeExceMax as error:
                return JsonResponse({"error": f'El nivel del arbol excede el rango permitido de {NODE_LEVEL}'},
                                    status=HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({"error": f'El id {node_id} no pertenece a ningun nodo'},
                            status=HTTP_400_BAD_REQUEST)

        data_out = tree.root.to_dict()
        return JsonResponse({"success": data_out},
                        status=HTTP_200_OK)