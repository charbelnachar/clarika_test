from django.urls import path

from clarika.apps.tree.logic import AddNodeTreeView
from clarika.apps.tree.logic import DeletedNodeView
from clarika.apps.tree.logic import EditValueNodeView
from clarika.apps.tree.logic import GetNodeStructView
from clarika.apps.tree.logic import NewSubtreeSpecificNodeView
from clarika.apps.tree.logic import RestoreNodeView


app_name = 'Auth'

urlpatterns = [
        path('agregar_sub_arbol_nodo/', NewSubtreeSpecificNodeView.as_view()),
        path('agregar_nodo_valor/', AddNodeTreeView.as_view()),
        path('editar_valor_nodo/', EditValueNodeView.as_view()),
        path('borrar_nodo/', DeletedNodeView.as_view()),
        path('restaurar_nodo/', RestoreNodeView.as_view()),
        path('devolver_arbol/', GetNodeStructView.as_view()),
        ]
