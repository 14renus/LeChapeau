from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateRoomView, name='create_room'),
    path('<str:room_id>/', views.AddPlayerView, name='add_players'),
    path('<str:room_id>/<str:player_id>/', views.StartGameView, name='start_game')
]