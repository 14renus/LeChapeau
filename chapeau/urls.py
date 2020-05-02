from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateRoom, name='create_room'),
    path('post/<str:room_id>/', views.AddPlayer, name='add_players'),
]