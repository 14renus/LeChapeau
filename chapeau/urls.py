from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_room, name='create_room'),
    path('post/<str:salle_id>/', views.add_players, name='add_players'),
]