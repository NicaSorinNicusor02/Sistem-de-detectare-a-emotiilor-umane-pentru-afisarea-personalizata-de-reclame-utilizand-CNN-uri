from django.shortcuts import render
from django.views.generic import CreateView
from django.http import JsonResponse
from django.urls import reverse_lazy
import json
from .models import CustomUser
from .forms import SHOPPING_CENTERS, CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #adauga centrele comerciale ca JSON(format de schimb de date care utilizeaza text) in contextul templateului
        context['shopping_centers_json'] = json.dumps(SHOPPING_CENTERS)#converteste structura de date sub 
        #forma de dictionar intr-un sir de caractere in format JSON, este utilizat mai tarziu in register.htmlS
        return context


def get_shopping_centers(request):
    city = request.GET.get('city', None)
    if city in SHOPPING_CENTERS:
        # returneaza lista de centre comerciale pentru orasul selectat
        return JsonResponse(SHOPPING_CENTERS[city], safe=False)
    return JsonResponse([], safe=False)