from django.http import HttpResponse
from django.views import View

class SaludoView(View):
    def get(self, request):
        
        return HttpResponse('¡Hola, mundo!')