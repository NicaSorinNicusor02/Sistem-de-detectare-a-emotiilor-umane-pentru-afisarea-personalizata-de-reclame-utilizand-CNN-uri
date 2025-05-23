from django.urls import path
from .views import SignUpView
from .views import get_shopping_centers
from . import views

urlpatterns = [
    path("register/", SignUpView.as_view(), name="register"),
    path('get_shopping_centers/', views.get_shopping_centers, name='get_shopping_centers'),
]