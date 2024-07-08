from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('watch_movie/', views.watch_movie, name='watch_movie'),
    path('search/', views.search, name='search'),
]
