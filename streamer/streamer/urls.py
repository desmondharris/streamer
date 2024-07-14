from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('home.urls')),
    path('profile/', include('home.urls')),
    path('add_to_list/', include('home.urls')),
    path('<str:imdb_id>/', include('home.urls')),
    path('<str:imdb_id>/<int:season>/', include('home.urls')),
]
