from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from PyMovieDb import IMDB
import tmdbsimple as tmdb


@login_required
def home(request):
    return render(request, 'home.html')

def search(request):
    print("search view")
    db = IMDB()
    tmdb.API_KEY = '16d0db51d9356bcbecc06f57c1c0e593'
    searcher = tmdb.Search()
    conf = tmdb.Configuration().info()
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', '')
    if search_type == 'movieSearch':
        searcher.movie(query=query)
        media_type = 'movie'
    elif search_type == 'tvSearch':
        searcher.tv(query=query)
        media_type = 'tv'
    output = []
    for s in searcher.results:
        result = {}
        result['title'] = s['title']
        result['id'] = s['id']
        result['year'] = s['release_date'].split('-')[0]
        result["poster"] = f"{conf['images']['base_url']}w185{s['poster_path']}"
        result["media_type"] = media_type
        output.append(result)
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


def watch_movie(request):
    pass