from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateRoomView, name='create_room'),
    path('<str:room_id>/', views.AddPlayerView, name='add_players'),
    path('<str:room_id>/<str:player_id>/', views.StartGameView, name='start_game'),
    path('<str:room_id>/<str:player_id>/guesser', views.GuesserPreview, name='guesser'),
    path('<str:room_id>/<str:player_id>/hatter_preview', views.HatterPreview, name='hatter_preview'),
    path('<str:room_id>/<str:player_id>/hatter_round', views.HatterView, name='hatter_round'),
    path('<str:room_id>/<str:player_id>/round_results', views.RoundResultsView, name='round_results'),
    path('<str:room_id>/<str:player_id>/game_over', views.EndGameView, name='game_over'),
]