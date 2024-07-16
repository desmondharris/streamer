from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('profile', views.profile, name='profile'),
    path('add_to_list', views.add_to_list, name='add_to_list'),
    path('movie/<str:imdb_id>/', views.movie_player, name='movieplayer'),
    path('tv/<str:imdb_id>/', views.tv_player, name='tvplayer'),
    path('search/<str:search_query>/', views.search, name='search')
]
