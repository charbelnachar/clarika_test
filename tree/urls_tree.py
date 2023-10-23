from django.urls import path
from django.urls import re_path

from tree.logic import SaludoView

# from rest_framework_jwt.views import obtain_jwt_token

app_name = 'Auth'

urlpatterns = [
    path('saludo/', SaludoView.as_view()),
]