from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreerSalle, name='creer_salle'),
    path('post/<str:salle_id>/', views.AjouteJoeurs, name='ajoute_jouers'),
]