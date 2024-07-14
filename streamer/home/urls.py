from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('profile', views.profile, name='profile'),
    path('add_to_list', views.add_to_list, name='add_to_list'),
    path('<str:imdb_id>/', views.movie_player, name='movieplayer'),
    path('<str:imdb_id>/<int:season>/', views.tv_player, name='tvplayer'),
    path('<str:imdb_id>/search/', views.search, name='movieplayer'),
    path('<str:imdb_id>/<int:season>/search/', views.search, name='tvplayer'),
]
