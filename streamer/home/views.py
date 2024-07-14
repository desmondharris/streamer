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
    if request.GET.get("media_type"):
        media_type = request.GET.get("media_type")
        imdb_id = request.GET.get("id")
        if request.get("season"):
            season = request.GET.get("season")
    else:
        media_type = "default"
        imdb_id = -1
        season = -1
    return render(request, 'home.html', {'media_type': media_type, 'imdb_id': imdb_id, season: season})


def movie_player(request, imdb_id):
    return render(request, 'player.html', {'media_type': "movie", 'imdb_id': imdb_id})


def tv_player(request, imdb_id, season):
    return render(request, 'player.html', {'media_type': "tv", 'imdb_id': imdb_id, 'season': season})


def search(request):
    print("search view")
    db = IMDB()
    searcher = tmdb.Search()
    conf = tmdb.Configuration().info()
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', '')
    output = []
    if search_type == 'movieSearch':
        searcher.movie(query=query)
        media_type = 'movie'
        for s in searcher.results:
            result = {}
            result['title'] = s['title']
            result['id'] = s['id']
            result['year'] = s['release_date'].split('-')[0]
            result["poster"] = f"{conf['images']['base_url']}w185{s['poster_path']}"
            result["media_type"] = media_type
            output.append(result)
    elif search_type == 'tvSearch':
        result = {}
        searcher.tv(query=query)
        media_type = 'tv'
        for s in searcher.results:
            result = {}
            result['title'] = s['name']
            result['id'] = s['id']
            result['year'] = s['first_air_date'].split('-')[0]
            result["poster"] = f"{conf['images']['base_url']}w185{s['poster_path']}"
            result["media_type"] = media_type
            output.append(result)
            print(result)

    print(output)
    return JsonResponse({"results": output})
    # print(len(results))
    # for result in results:
    #     # print all the results
    #     if search_type == 'movieSearch':
    #         print(f"title: {result['title']}, year: {result['year']}, id: {result['id']}, leads: {result['leads']}, type: {result['media_type']}\nposter: {result['poster']}\n")
    #     print(f"title: {result['title']}, year: {result['year']}, id: {result['id']}, leads: {result['leads']}, type: {result['media_type']}\nposter: {result['poster']}\n")
    # return JsonResponse({"results": results})


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