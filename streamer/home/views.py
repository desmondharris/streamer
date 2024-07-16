from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import WatchedMovie, WatchedTV

from PyMovieDb import IMDB
import tmdbsimple as tmdb
tmdb.API_KEY = '16d0db51d9356bcbecc06f57c1c0e593'

@login_required
def home(request):
    return render(request, 'home.html')


def movie_player(request, imdb_id):
    print(f"loading movie {imdb_id}")
    return render(request, 'player.html', {'media_type': "movie", 'imdb_id': imdb_id})


def tv_player(request, imdb_id):
    print(f"loading tv show {imdb_id}")
    return render(request, 'player.html', {'media_type': "tv", 'imdb_id': imdb_id})


def search(request, search_query):
    import random
    print("search view")
    searcher = tmdb.Search()
    conf = tmdb.Configuration().info()
    query = search_query
    output = []

    searcher.movie(query=query)
    media_type = 'movie'
    for s in searcher.results:
        result = {}
        result['title'] = s['title']
        result['id'] = s['id']
        result['year'] = s['release_date'].split('-')[0]
        result["poster"] = f"{conf['images']['base_url']}w185{s['poster_path']}"
        result["media_type"] = media_type
        result["popularity"] = s['popularity']
        output.append(result)

    searcher.tv(query=query)
    media_type = 'tv'
    for s in searcher.results:
        result = {}
        result['title'] = s['name']
        result['id'] = s['id']
        result['year'] = s['first_air_date'].split('-')[0]
        result["poster"] = f"{conf['images']['base_url']}w185{s['poster_path']}"
        result["media_type"] = media_type
        result["popularity"] = s['popularity']
        output.append(result)

    output = sorted(output, key=lambda x: x['popularity'], reverse=True)
    print(output)
    return render(request, 'search.html', {'results': output})
    # return JsonResponse({"results": output})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('player')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def add_to_list(request):
    if request.method == 'POST':
        user = request.user
        imdb_id = request.POST['id']
        media_type = request.POST['media_type']
        conf = tmdb.Configuration().info()
        if media_type == 'movie':
            mov = tmdb.Movies(imdb_id)
            mov = mov.info()
            WatchedMovie.objects.create(user=user, imdb_id=imdb_id, title=mov['title'], year=mov['release_date'].split('-')[0], poster=f"{conf['images']['base_url']}w185{mov['poster_path']}")
            print(f"Added {imdb_id} to {user.username}'s watched movies")
        elif media_type == 'tv':
            tvshow = tmdb.TV(imdb_id)
            tvshow = tvshow.info()
            WatchedTV.objects.create(user=user, title=tvshow["name"], imdb_id=imdb_id, season=request.POST['season'], year=tvshow['first_air_date'].split('-')[0], poster=f"{conf['images']['base_url']}w185{tvshow['poster_path']}")
            print(f"Added {imdb_id} to {user.username}'s watched tv")
        return JsonResponse({"status": "success"})
    print("fail")
    return JsonResponse({"status": "403"})


def profile(request):
    user = request.user
    movies = WatchedMovie.objects.filter(user=user)
    tvshows = WatchedTV.objects.filter(user=user)
    print(tvshows)
    movies = [{"title": m.title, "year": m.year, "poster": m.poster, "imdb_id": m.imdb_id, "media_type": "movie"} for m in movies]
    return render(request, 'profile.html', {'movies': movies, 'tvshows': tvshows})