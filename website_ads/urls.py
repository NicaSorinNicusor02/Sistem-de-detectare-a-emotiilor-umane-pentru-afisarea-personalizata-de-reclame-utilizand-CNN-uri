from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
from .views import open_ticket
from .views import delete_ad

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('accounts/', include('django.contrib.auth.urls')), 
    path("", TemplateView.as_view(template_name="home.html"), name="home"),

    #ruta pentru pagina "reclamele mele"
    path('ads/', views.ads_list, name='ads_list'),
    
    # ruta pentru "Incarca o reclama noua"
    path('upload/', views.upload_ad, name='upload_ad'),
    
    #ruta pentru deschiderea tichetului
    path("open_ticket/", views.open_ticket, name="open_ticket"),
    path('success/', views.success_page, name='success_page'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),

    path('ads/delete/<int:ad_id>/', delete_ad, name='delete_ad'),

    path('emotion-detection/', views.launch_emotion_detection, name='emotion_detection'),

    path('rosetta/', include('rosetta.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)